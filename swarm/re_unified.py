#!/usr/bin/env python3
"""
swarm/re_unified.py
Unified reverse-engineering pipeline combining eight skills (Ghidra excluded):
  ImHex (entropy/format triage), radare2/Rizin (functions/strings/imports),
  rev.ng (decompilation), Frida (dynamic hooks), x64dbg (PE command scripts),
  REA (structured JSON), awesome catalogs (niche tool suggestions),
  methodology (static-first ordering + safety notes).
Readelf/objdump fallbacks keep the pipeline alive without radare2.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "reports" / "re"
LOG_DIR = ROOT / "logs" / "re"

SKILLS = {
    "imhex": "entropy + format triage",
    "radare2": "functions, strings, imports, xrefs",
    "rizin": "radare2 fork, same analysis surface",
    "revng": "decompilation to C",
    "frida": "dynamic hooks + runtime tracing",
    "x64dbg": "PE debugging command scripts",
    "rea": "structured JSON findings payload",
    "awesome": "niche tool suggestions by target type",
    "methodology": "static-first ordering, safety gates",
}

METHODOLOGY = [
    "1. Static first: never run unknown binaries before triage.",
    "2. ImHex entropy scan catches packers/encryption early.",
    "3. readelf/objdump fallback if radare2 absent.",
    "4. rev.ng decompile only after static map is built.",
    "5. Frida hooks require a running instance and target consent.",
    "6. x64dbg scripts are PE-only; refuse ELF.",
    "7. REA JSON is the handoff format for downstream agents.",
    "8. Awesome catalogs flag malware-ish strings as false-positive-prone.",
    "9. Safety: no mainnet interaction, no credential dumping, log everything.",
]

AWESOME_MAP = {
    "elf": ["checksec", "pwntools", "ropper", "one_gadget"],
    "pe": ["pefile", "capa", "scyllaHide", "Scylla"],
    "macho": ["MachOView", "class-dump", "Hopper"],
    "wasm": ["wasm2wat", "wabt", "wasmtime"],
    "apk": ["apktool", "jadx", "frida-dexdump"],
    "firmware": ["binwalk", "firmadyne", "EMBA"],
    "malware": ["CAPE", "Cuckoo", "YARA", "FLOSS"],
    "web": ["Burp", "nuclei", "httpx", "ffuf"],
    "smart_contract": ["slither", "mythril", "echidna"],
    "blockchain": ["heimdall-rs", "cast", "foundry"],
}


def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def run(cmd: list[str], timeout: int = 60) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -2, "", f"not found: {cmd[0]}"


def imhex_triage(path: Path) -> dict:
    data = path.read_bytes()[:2_000_000]
    if not data:
        return {"error": "empty file"}
    from collections import Counter
    freq = Counter(data)
    total = len(data)
    import math
    ent = -sum((c / total) * math.log2(c / total) for c in freq.values() if c)
    mx = max(freq.values()) / total
    magic = data[:4]
    fmt = "unknown"
    if magic.startswith(b"\x7fELF"):
        fmt = "ELF"
    elif magic[:2] == b"MZ":
        fmt = "PE"
    elif magic[:4] == b"\xcf\xfa\xed\xfe":
        fmt = "Mach-O 64-bit"
    elif magic[:4] == b"\xca\xfe\xba\xbe":
        fmt = "Mach-O universal"
    elif data[:4] == b"\x00asm":
        fmt = "WASM"
    return {"tool": "imhex", "format": fmt, "entropy_mean": round(ent, 3),
            "entropy_max_byte_ratio": round(mx, 3), "packed_suspected": ent > 7.2,
            "size_bytes": path.stat().st_size}


def readelf_fallback(path: Path) -> dict:
    out = {"tool": "readelf", "available": have("readelf")}
    if not out["available"]:
        return out
    rc, so, se = run(["readelf", "-h", str(path)])
    if rc == 0:
        for line in so.splitlines():
            if "Class:" in line:
                out["class"] = line.split(":", 1)[1].strip()
            if "Machine:" in line:
                out["machine"] = line.split(":", 1)[1].strip()
            if "Entry point" in line:
                out["entry"] = line.split(":", 1)[1].strip()
    rc, so, se = run(["readelf", "-S", str(path)])
    if rc == 0:
        out["sections"] = len([l for l in so.splitlines() if l.strip().startswith("[")])
    return out


def objdump_fallback(path: Path) -> dict:
    out = {"tool": "objdump", "available": have("objdump")}
    if not out["available"]:
        return out
    rc, so, se = run(["objdump", "-d", str(path)], timeout=120)
    if rc == 0:
        out["functions"] = sum(1 for l in so.splitlines() if "<" in l and ">:" in l)
    rc, so, se = run(["objdump", "-T", str(path)])
    if rc == 0:
        out["dyn_symbols"] = len([l for l in so.splitlines() if l.strip() and not l.startswith(" ")][:500])
    return out


def radare_analysis(path: Path) -> dict:
    out = {"tool": "radare2", "available": have("r2")}
    if not out["available"]:
        out["tool"] = "rizin"
        out["available"] = have("rizin")
        bin_ = "rizin"
    else:
        bin_ = "r2"
    if not out["available"]:
        return out
    rc, so, se = run([bin_, "-qc", "aaa; afl; iz; ii", str(path)], timeout=180)
    if rc != 0:
        out["error"] = se[:500]
        return out
    lines = so.splitlines()
    out["functions"] = [l for l in lines if l.strip()[:1].isdigit()]
    out["strings"] = [l for l in lines if "str." in l][:200]
    out["imports"] = [l for l in lines if "imp." in l][:100]
    sens = []
    for l in out["strings"]:
        low = l.lower()
        for kw in ("password", "secret", "api_key", "token", "private", "wallet", "mnemonic"):
            if kw in low:
                sens.append(l.strip())
                break
    out["sensitive_strings"] = sens[:50]
    return out


def revng_decompile(path: Path) -> dict:
    out = {"tool": "revng", "available": have("revng")}
    if not out["available"]:
        return out
    rc, so, se = run(["revng", "decompile", str(path)], timeout=300)
    out["rc"] = rc
    if rc == 0:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        p = OUT_DIR / (path.name + ".c")
        p.write_text(so)
        out["decompiled_to"] = str(p)
        out["lines"] = len(so.splitlines())
    else:
        out["error"] = se[:500]
    return out


def frida_hooks(path: Path, duration: int = 10) -> dict:
    out = {"tool": "frida", "available": have("frida"), "note": "requires running target"}
    if not out["available"]:
        return out
    script = (
        'Interceptor.attach(Module.findExportByName(null, "open"), {\n'
        '  onEnter(args) { send({api:"open", path: args[0].readUtf8String()}); }\n'
        '});\n'
        'Interceptor.attach(Module.findExportByName(null, "connect"), {\n'
        '  onEnter(args) { send({api:"connect"});} });\n'
    )
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    sp = OUT_DIR / (path.name + ".frida.js")
    sp.write_text(script)
    out["script_written"] = str(sp)
    out["status"] = "script_ready_not_executed"
    return out


def x64dbg_script(path: Path) -> dict:
    out = {"tool": "x64dbg", "applicable": False}
    data = path.read_bytes()[:4]
    if data[:2] != b"MZ":
        out["note"] = "not a PE, skipped"
        return out
    out["applicable"] = True
    lines = ["bpx entrypoint", "run", "info", "mod", "bp*"]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUT_DIR / (path.name + ".x64dbg.txt")
    p.write_text("\n".join(lines))
    out["script_written"] = str(p)
    return out


def rea_payload(results: dict) -> dict:
    return {
        "tool": "rea",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": results.get("target"),
        "triage": results.get("imhex"),
        "static": results.get("radare") or results.get("readelf") or results.get("objdump"),
        "dynamic": results.get("frida"),
        "decompile": results.get("revng"),
        "debugger": results.get("x64dbg"),
        "findings_count": len(results.get("radare", {}).get("sensitive_strings", [])),
        "safety_notes": METHODOLOGY[-2:],
    }


def awesome_suggest(fmt: str) -> dict:
    key = fmt.lower().split()[0] if fmt else "unknown"
    return {"tool": "awesome", "format": fmt,
            "suggested": AWESOME_MAP.get(key, AWESOME_MAP.get("elf", []))}


def analyze(path: Path) -> dict:
    results = {"target": str(path), "started": datetime.now(timezone.utc).isoformat()}
    results["imhex"] = imhex_triage(path)
    fmt = results["imhex"].get("format", "unknown")
    results["readelf"] = readelf_fallback(path)
    results["objdump"] = objdump_fallback(path)
    results["radare"] = radare_analysis(path)
    results["revng"] = revng_decompile(path)
    results["frida"] = frida_hooks(path)
    results["x64dbg"] = x64dbg_script(path)
    results["awesome"] = awesome_suggest(fmt)
    results["rea"] = rea_payload(results)
    results["methodology"] = METHODOLOGY
    results["finished"] = datetime.now(timezone.utc).isoformat()
    return results


def write_report(results: dict, md: bool):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    stem = Path(results["target"]).name
    jp = OUT_DIR / (stem + ".json")
    jp.write_text(json.dumps(results, indent=2))
    print(f"JSON: {jp}")
    if md:
        mp = OUT_DIR / (stem + ".md")
        lines = [f"# RE Report: {stem}", "", f"- Format: {results['imhex'].get('format')}",
                 f"- Entropy: {results['imhex'].get('entropy_mean')}",
                 f"- Functions (objdump): {results['objdump'].get('functions', 'n/a')}",
                 f"- Radare2: {'yes' if results['radare'].get('available') else 'no'}",
                 f"- Sensitive strings: {len(results['radare'].get('sensitive_strings', []))}",
                 "", "## Methodology", ""]
        lines += ["- " + m for m in METHODOLOGY]
        mp.write_text("\n".join(lines))
        print(f"MD: {mp}")


def main():
    ap = argparse.ArgumentParser(description="Unified RE pipeline (no Ghidra)")
    ap.add_argument("target", help="binary to analyze")
    ap.add_argument("--md", action="store_true", help="also write markdown report")
    ap.add_argument("--frida-run", action="store_true", help="execute frida (needs live target)")
    args = ap.parse_args()
    path = Path(args.target)
    if not path.exists():
        print(f"not found: {path}", file=sys.stderr)
        sys.exit(1)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(LOG_DIR / "runs.jsonl", "a") as f:
        f.write(json.dumps({"ts": datetime.now(timezone.utc).isoformat(),
                            "target": str(path)}) + "\n")
    results = analyze(path)
    write_report(results, args.md)
    r = results["radare"]
    print(f"format={results['imhex'].get('format')} "
          f"entropy={results['imhex'].get('entropy_mean')} "
          f"functions={results['objdump'].get('functions', 'n/a')} "
          f"strings={len(r.get('strings', []))} "
          f"sensitive={len(r.get('sensitive_strings', []))}")


if __name__ == "__main__":
    main()
