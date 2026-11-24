#!/usr/bin/env python3
"""Minimal context compressor. Strips whitespace, truncates long fields,
replaces repeated boilerplate with placeholders, caps total size.
Drop-in for headroom.compress_outputs when the real package can't install."""
import json, re, sys

MAX = 4000
BOILER = [(re.compile(r'https?://\S+'), '<url>'),
          (re.compile(r'[A-Za-z0-9+/]{40,}={0,2}'), '<b64>'),
          (re.compile(r'(?m)^ {4,}'), '  ')]

def compact(text, limit=MAX):
    if not isinstance(text, str): text = json.dumps(text, default=str)
    for rx, rep in BOILER: text = rx.sub(rep, text)
    text = re.sub(r'\n{3,}', '\n\n', text).strip()
    return text[:limit] + ('\n...[truncated]' if len(text) > limit else '')

if __name__ == '__main__':
    print(compact(sys.stdin.read()))