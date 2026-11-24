# Blockchain & Crypto Bug Bounty Digest: Top 5 Bugcrowd Targets

**Generated:** 2026-11-24  
**Scope:** Active public Bugcrowd programs involving blockchain, smart contracts, wallets, or DeFi.  
**Methodology:** Public information only (program briefs, GitHub, audit reports). Conceptual reverse-engineering of public bytecode/source and known vulnerability classes. **No exploitation, no submissions, no private data.**

Vulnerability scoring (0-10, higher = more residual risk surface for that class based on public architecture, audit history, and typical attack vectors):
- **Reentrancy**: External calls before state updates.
- **Access Control**: Missing/weak modifiers, ownership, roles.
- **Oracle Manipulation**: Price feeds, external data reliance.
- **Signature Replay**: Nonce/domain separator issues, cross-chain or multi-sig.

## Ranked Top 5 Targets

### 1. OpenSea Managed Bug Bounty Program
- **Program URL:** https://bugcrowd.com/engagements/opensea
- **Max Reward:** $3,000,000 (Seaport P1)
- **Chains:** Ethereum (primary), Solana, multi-chain deployments
- **Public Contracts:**
  - Seaport 1.6: `0x0000000000000068F116a894984e2DB1123eB395`
  - ConduitController: `0x00000000F9490004C11Cef243f5400493c00Ad63`
  - OpenSea Conduit: `0x1e0049783f008a0085193e00003d00cd54003c71`
  - Fee Collector: `0x0000a26b00c1F0DF003000390027140000fAa719`
  - SeaDrop: `0x00005EA00Ac477B1030CE78506496e8C2dE24bf5`
  - Solana Marketplace Program: `7Aru291A64wrTkUDaRv6HqxVBre6ivXWL94cUoCtQF9V`
- **Audit Reports:** Trail of Bits (Seaport, May 2022); Spearbit (SeaDrop); public on GitHub.
- **Conceptual RE:** Source fully public (ProjectOpenSea/seaport, seadrop). Bytecode verifiable on Etherscan. Complex order fulfillment with consideration items, zones, and conduits.
- **Scores:**
  - Reentrancy: 4/10 (heavy use of external calls in fulfillment; mitigated by audits and CEI patterns)
  - Access Control: 6/10 (zone authorizers, fee recipients, conduit ownership)
  - Oracle Manipulation: 2/10 (limited; mostly NFT marketplace, not price oracles)
  - Signature Replay: 7/10 (EIP-712 order signatures, counterfactual, multi-version deployments)
- **Evidence:** Highest advertised payout on Bugcrowd. Explicit in-scope smart contracts with pure on-chain focus. Mature but high-value target with ongoing deployments.

### 2. Fireblocks MPC Managed Bug Bounty Engagement
- **Program URL:** https://bugcrowd.com/engagements/fireblocks-mbb-og2
- **Max Reward:** $150,000
- **Chains:** Multi-chain (ECDSA/EdDSA for Bitcoin, Ethereum, etc.)
- **Public Code:** https://github.com/fireblocks/mpc-lib (C++ MPC library: CMP for ECDSA, EdDSA)
- **Audit Reports:** NCC Group (referenced in SECURITY.md)
- **Conceptual RE:** Full source public. Focus on cryptographic protocol implementation rather than bytecode. Threat model documented in SECURITY-MODEL.md.
- **Scores:**
  - Reentrancy: 1/10 (not smart-contract based)
  - Access Control: 5/10 (key shares, party roles in MPC)
  - Oracle Manipulation: 1/10 (N/A)
  - Signature Replay: 9/10 (core signature generation; rogue signatures, key extraction)
- **Evidence:** Active public program on cryptographic library. Critical findings defined around key retrieval or rogue signatures. High recent activity.

### 3. Immutable Bug Bounty (Passport)
- **Program URL:** https://bugcrowd.com/engagements/immutable
- **Max Reward:** $10,000 (P1 for Passport)
- **Chains:** Immutable zkEVM (primary), Immutable X
- **Public Contracts:** Smart Contract Wallets (SCW) from https://github.com/immutable/wallet-contracts (fork of Sequence). Counterfactual CREATE2 deployment. 2-of-2 multisig (User Key via Magic + Guardian).
- **Audit Reports:** Trail of Bits, Halborn, Consensys Diligence / Quantstamp (upstream Sequence), Halborn customizations (2023).
- **Conceptual RE:** Source public. Wallet logic, relayer co-signing, Guardian modal, pre-authorized transactions.
- **Scores:**
  - Reentrancy: 5/10 (wallet execution paths)
  - Access Control: 7/10 (2-of-2, organization roles in Dev Hub, Guardian policies)
  - Oracle Manipulation: 2/10 (limited)
  - Signature Replay: 8/10 (multi-sig, Magic key binding, EIP-1193 linking)
- **Evidence:** Explicit focus on Passport wallet properties that must hold (key isolation, co-signing, confirmation screen integrity). Public contracts and architecture docs.

### 4. Electroneum Smart Chain (ETN-SC)
- **Program URL:** https://bugcrowd.com/engagements/smartchain-mbb-og
- **Max Reward:** $12,000
- **Chains:** Electroneum Smart Chain (EVM-compatible L1, IBFT consensus, ~5s blocks)
- **Public Code:** https://github.com/electroneum/electroneum-sc/ (go-ethereum fork with IBFT)
- **Audit Reports:** Hacken (bridge and overall 10/10 security score referenced); full source available.
- **Conceptual RE:** Entire client source public. Consensus, RPC, validator voting, cross-chain bridge components. Bytecode of any system contracts inspectable via explorer.
- **Scores:**
  - Reentrancy: 6/10 (any custom contracts or bridge)
  - Access Control: 7/10 (validator set management, governance)
  - Oracle Manipulation: 3/10 (limited native oracles)
  - Signature Replay: 5/10 (transaction and validator signatures)
- **Evidence:** Full open-source L1. Eligible outcomes explicitly include minting, consensus gaming, private key exposure. Recent activity on program.

### 5. Binance (incl. Trust Wallet & BSC surfaces)
- **Program URL:** https://bugcrowd.com/engagements/binance
- **Max Reward:** $100,000
- **Chains:** BNB Smart Chain, multi-chain wallet support
- **Public Elements:** Trust Wallet Android/iOS/Chrome Extension in scope; related BSC GitHub repos (bsc, genesis contracts, relayers) historically referenced.
- **Audit Reports:** Not centralized in brief; Trust Wallet has independent audits historically.
- **Conceptual RE:** Mobile wallet binaries (APK/IPA) for reverse-engineering of key storage, signing logic. Web3 components.
- **Scores:**
  - Reentrancy: 3/10 (app-layer more than contracts)
  - Access Control: 6/10 (wallet permissions, remote key exposure)
  - Oracle Manipulation: 4/10 (possible in related DeFi surfaces)
  - Signature Replay: 7/10 (transaction signing implementations)
- **Evidence:** Large surface including official Trust Wallet apps. Focus areas include remote loss of funds and private key exposure. High volume of rewarded vulnerabilities historically.

## Summary Ranking Rationale
1. **OpenSea** — Extreme reward + verified on-chain contracts with signature-heavy design.
2. **Fireblocks MPC** — High-value cryptographic implementation with clear critical impact definitions.
3. **Immutable Passport** — Production smart-contract wallet with multi-party signing.
4. **Electroneum SC** — Fully open L1 source with consensus and minting impact categories.
5. **Binance/Trust Wallet** — Broad wallet binary surface and high max payout.

**Disclaimer:** All analysis is based on publicly available program briefs, source repositories, and audit summaries as of 2026-11-24. Scores are conceptual residual-risk indicators only. No vulnerabilities were exploited or reported. Researchers must follow each program’s official rules and safe harbor.
