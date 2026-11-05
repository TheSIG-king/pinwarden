# Sourced facts for the README "Why" section (verified 2026-11-05)

Rules: every claim has a link. CVE data comes from the NVD API (`services.nvd.nist.gov/rest/json/cves/2.0?cveId=…`) on 2026-11-05, and CVSS is the first score NVD lists (v3.1 where present). Anything we could not confirm against a primary source is marked **UNVERIFIED**. Do not copy UNVERIFIED items into the README.

## (a) MCP vulnerability wave: concrete CVEs

| CVE | Component | NVD published | CVSS | Summary (from NVD) | Link |
|---|---|---|---|---|---|
| CVE-2025-6514 | `mcp-remote` | 2025-07-09 | 9.6 | OS command injection when connecting to untrusted MCP servers, via crafted `authorization_endpoint` | https://nvd.nist.gov/vuln/detail/CVE-2025-6514 |
| CVE-2025-49596 | MCP Inspector < 0.14.1 | 2025-06-13 | 9.4 | RCE due to lack of authentication between Inspector client and proxy | https://nvd.nist.gov/vuln/detail/CVE-2025-49596 · [Oligo write-up](https://www.oligo.security/blog/critical-rce-vulnerability-in-anthropic-mcp-inspector-cve-2025-49596) |
| CVE-2025-53109 / CVE-2025-53110 | Reference Filesystem MCP server < 0.6.4 / 2025.7.01 | 2025-07-02 | 7.3 / 7.3 | Symlink escape / path-prefix bypass of allowed directories | https://nvd.nist.gov/vuln/detail/CVE-2025-53109 · https://nvd.nist.gov/vuln/detail/CVE-2025-53110 |
| CVE-2025-54136 | Cursor ≤ 1.2.4 | 2025-08-02 | 7.2 | Persistent RCE by modifying an already-trusted MCP config in a shared repo | https://nvd.nist.gov/vuln/detail/CVE-2025-54136 |
| CVE-2025-54994 | `@akoskm/create-mcp-server-stdio` < 0.0.13 | 2025-09-08 | 9.3 | Command injection in stdio MCP server starter kit | https://nvd.nist.gov/vuln/detail/CVE-2025-54994 |
| CVE-2025-53967 | Framelink Figma MCP Server < 0.6.3 | 2025-10-08 | 8.0 | Unauthenticated remote OS command execution via shell metacharacters | https://nvd.nist.gov/vuln/detail/CVE-2025-53967 |
| CVE-2025-68143 / -68144 / -68145 | Reference `mcp-server-git` | 2025-12-17 | 8.8 / 7.1 / 9.1 | Arbitrary path in `git_init`; argument (flag) injection in `git_diff`/`git_checkout`; `--repository` restriction not enforced on `repo_path` | https://nvd.nist.gov/vuln/detail/CVE-2025-68143 · https://nvd.nist.gov/vuln/detail/CVE-2025-68144 · https://nvd.nist.gov/vuln/detail/CVE-2025-68145 |
| CVE-2026-21852 | Claude Code < 2.0.65 | 2026-01-21 | 7.5 | Malicious repo could exfiltrate data incl. API keys before trust confirmation | https://nvd.nist.gov/vuln/detail/CVE-2026-21852 |
| CVE-2026-0755 | `gemini-mcp-tool` | 2026-01-23 | 9.8 | `execAsync` command injection → unauthenticated RCE | https://nvd.nist.gov/vuln/detail/CVE-2026-0755 |
| CVE-2026-33032 | nginx-ui ≤ 2.3.5 (MCP integration) | 2026-03-30 | 9.8 | `/mcp_message` endpoint lacked the authentication applied to `/mcp` | https://nvd.nist.gov/vuln/detail/CVE-2026-33032 |
| CVE-2026-5058 | `aws-mcp-server` | 2026-04-11 | 9.8 | Command injection → unauthenticated RCE | https://nvd.nist.gov/vuln/detail/CVE-2026-5058 |
| CVE-2026-30615 | Windsurf 1.9544.26 | 2026-04-15 | 8.0 | Prompt injection from attacker-controlled HTML → arbitrary command execution | https://nvd.nist.gov/vuln/detail/CVE-2026-30615 |
| CVE-2026-30623 | LiteLLM | 2026-07-15 | 9.8 | RCE through MCP server creation (arbitrary command in stdio server JSON config) | https://nvd.nist.gov/vuln/detail/CVE-2026-30623 |

Note: CVE-2025-59536 (Claude Code < 1.0.111, CVSS 8.8, [NVD](https://nvd.nist.gov/vuln/detail/CVE-2025-59536)) is a trust-dialog code-injection bug. It is agent-adjacent rather than MCP-specific, so do not cite it as an MCP CVE.

**Systemic STDIO issue (OX Security, 2026-04-15).** OX Security published "The Mother of All AI Supply Chains". It argues that the MCP SDKs' STDIO transport allows arbitrary OS command execution wherever an attacker can influence the spawn command, and that Anthropic treats this as expected behaviour ([OX Security](https://www.ox.security/research-news/the-mother-of-all-ai-supply-chains-critical-systemic-vulnerability-at-the-core-of-the-mcp/), [CSA research note](https://labs.cloudsecurityalliance.org/research/csa-research-note-mcp-sdk-rce-by-design-20260422-csa-styled/), [SecurityWeek](https://www.securityweek.com/by-design-flaw-in-mcp-could-enable-widespread-ai-supply-chain-attacks/)). The CSA note cites "at least 14" downstream vulnerabilities with "10+" CVE IDs, including CVE-2026-30623 and CVE-2026-30615.
- **UNVERIFIED:** the exact CVE count, the "150M+ downloads" figure and the "200,000 servers" figure. These come from secondary coverage, and we did not read the full OX advisory table.
- **UNVERIFIED:** aggregate counts such as "30 CVEs in 60 days" ([agent-wars](https://agent-wars.com/news/2026-03-13-mcp-security-2026-30-cves-in-60-days-what-went-wrong)) or "95 MCP CVEs in 12 months" ([paperclipped](https://www.paperclipped.de/en/blog/mcp-cve-vulnerabilities-attack-surface/)). These are blogs with unclear methodology. Do not use them.

## (b) Studies on MCP servers without authentication

| Who / date | Sample | Exact finding | Link |
|---|---|---|---|
| Zhou, Zhang, Zhang, Zhang, Zhang, Yang, "A First Measurement Study on Authentication Security in Real-World Remote MCP Servers", arXiv:2605.22333v1, submitted 2026-05-21 | 7,973 live remote MCP servers | **40.55%** "expose tools without authentication". The raw count is ≈3,233; that figure is our arithmetic, not taken from the abstract. | https://arxiv.org/abs/2605.22333 |
| Knostic (Imri Goldberg), 2025-07-17 | 1,862 internet-exposed MCP servers found (Shodan + custom tooling); **119 manually verified** | "All 119 servers granted access to internal tool listings without authentication." The 100% applies to the 119-server sample only, not to all 1,862. | https://www.knostic.ai/blog/mapping-mcp-servers-study |
| Trend Micro (Alfredo Oliveira, David Fiser), update dated 2026-04-28 | Internet scan | Initial scan (July 2025): "492 confirmed instances running without any basic security controls" (no client auth or encryption). Update: exposed servers "nearly tripled to 1,467", 1,227 of them on legacy SSE. **No unauthenticated count is given for the 1,467.** | https://www.trendaisecurity.com/en-us/resources-insights/deep-research/update-on-exposed-mcp-servers-the-threat-widens-to-the-cloud |
| Backslash Security, June 2025 | not stated in sources reached | "Hundreds" of servers bound to 0.0.0.0 and "dozens" with network exposure plus no auth. **No percentage.** UNVERIFIED (primary page not read). | via [Descope summary](https://www.descope.com/blog/post/mcp-vulnerabilities) |

Recommended README phrasing: *"A May 2026 measurement of 7,973 live remote MCP servers found 40.55% exposed their tools without any authentication ([arXiv:2605.22333](https://arxiv.org/abs/2605.22333))."*
- **UNVERIFIED / do not use:** "73% of public MCP servers fail basic checks" ([agenticskills.io](https://agenticskills.io/learn/public-mcp-servers-security-audit)). This is an aggregator figure.

## (c) Attack classes: original sources

- **Tool Poisoning Attack (TPA).** Invariant Labs (Luca Beurer-Kellner, Marc Fischer), "MCP Security Notification: Tool Poisoning Attacks", 2025-04-01. Malicious instructions are embedded in tool descriptions, "invisible to users but visible to AI models". https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks
- **Rug pull.** The same Invariant post describes a server changing a tool description after the user approved it. Same URL as above.
- **Tool shadowing / cross-server.** The same Invariant post: a malicious server "injects a tool description that modifies the agent's behavior with respect to a trusted service or tool", even if its own tool is never called. Same URL as above.
- **Full-Schema Poisoning (FSP) and Advanced Tool Poisoning (ATPA).** CyberArk Labs (Simcha Kosman), "Poison everywhere: No output from your MCP server is safe", 2025-05-30. The attack surface extends to every schema field (parameter names, types, defaults, `required`), not just the description. ATPA poisons tool **outputs**. https://www.cyberark.com/resources/threat-research-blog/poison-everywhere-no-output-from-your-mcp-server-is-safe. Also presented at Nullcon Berlin 2025: https://nullcon.net/talk/your-mcp-server-executes-commands-but-from-whom/
- **Prior art on description pinning.** Invariant's mcp-scan "tool pinning" hashed tool descriptions to detect rug pulls: https://explorer.invariantlabs.ai/docs/mcp-scan
- **UNVERIFIED:** an original primary source specific to *invisible-Unicode* tool poisoning. Not researched in this pass; find one before citing.

## (d) EU AI Act: logging and traceability (Regulation (EU) 2024/1689)

- **Art. 12 "Record-keeping".** Para 1: "High-risk AI systems shall technically allow for the automatic recording of events (logs) over the lifetime of the system." Para 2 says this is done "in order to ensure a level of traceability of the functioning of a high-risk AI system…". https://artificialintelligenceact.eu/article/12/
- **Art. 19 "Automatically generated logs"** (providers). Logs are kept "for a period appropriate to the intended purpose … of at least six months", unless other Union or national law provides otherwise. https://artificialintelligenceact.eu/article/19/
- **Art. 26(6)** (obligations of deployers). "Deployers of high-risk AI systems shall keep the logs automatically generated by that high-risk AI system … of at least six months". https://artificialintelligenceact.eu/article/26/
- **Timing caveat.** The Digital Omnibus on AI postponed stand-alone Annex III high-risk obligations from 2 Aug 2026 to **2 Dec 2027**, and Annex I product-embedded systems to 2 Aug 2028 ([Orrick](https://www.orrick.com/en/Insights/2026/05/EUs-Digital-Omnibus-on-AI-7-Key-Changes-You-Need-to-Know), [Gibson Dunn](https://www.gibsondunn.com/eu-ai-act-omnibus-agreement-postponed-high-risk-deadlines-and-other-key-changes/), [Cuatrecasas: Council approval](https://www.cuatrecasas.com/en/latam/intellectual-property/art/council-eu-approves-digital-omnibus-ai)). **UNVERIFIED:** the OJ reference "Regulation (EU) 2026/1744" and its entry-into-force date of 27 July 2026. We did not check EUR-Lex.
- **README wording guidance.** These obligations apply to *high-risk* AI systems only. An MCP gateway is not itself "AI Act compliance". Say it "helps produce the automatic, retained event logs that Art. 12/19/26(6) require of high-risk systems".

## (e) OWASP lists (exact titles)

### OWASP MCP Top 10. Exists, **beta**
URL: https://owasp.org/www-project-mcp-top-10/ (GitHub: https://github.com/OWASP/www-project-mcp-top-10). Status on the page: "Phase 3 – Beta Release and Pilot Testing". The final release (Phase 4) has not shipped. The page states no version number. IDs carry the suffix `:2025`. License: CC BY-NC-SA 4.0 per the badge; the prose on the page says "Attribution-ShareAlike 4.0", which is inconsistent.

| ID | Title |
|---|---|
| MCP01:2025 | Token Mismanagement & Secret Exposure |
| MCP02:2025 | Privilege Escalation via Scope Creep |
| MCP03:2025 | Tool Poisoning |
| MCP04:2025 | Software Supply Chain Attacks & Dependency Tampering |
| MCP05:2025 | Command Injection & Execution |
| MCP06:2025 | Prompt Injection via Contextual Payloads |
| MCP07:2025 | Insufficient Authentication & Authorization |
| MCP08:2025 | Lack of Audit and Telemetry |
| MCP09:2025 | Shadow MCP Servers |
| MCP10:2025 | Context Injection & Over-Sharing |

Because it is beta, titles may change. Re-check before each release.

### OWASP Top 10 for Agentic Applications for 2026
Official page: https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/ (OWASP GenAI Security Project, dated 2025-12-09). The official page does not list the titles in HTML; they are in the downloadable PDF. The titles below come from [Giskard](https://www.giskard.ai/knowledge/owasp-top-10-for-agentic-application-2026) and are corroborated for ASI02, ASI03 and ASI07 by [Descope](https://www.descope.com/blog/post/owasp-agentic-top-10-identity) and [Modulos](https://docs.modulos.ai/frameworks/owasp-top-10-agentic). **Confirm against the official PDF before publishing.**

| ID | Title |
|---|---|
| ASI01 | Agent Goal Hijack |
| ASI02 | Tool Misuse and Exploitation |
| ASI03 | Identity and Privilege Abuse |
| ASI04 | Agentic Supply Chain Vulnerabilities |
| ASI05 | Unexpected Code Execution (RCE) |
| ASI06 | Memory & Context Poisoning |
| ASI07 | Insecure Inter-Agent Communication |
| ASI08 | Cascading Failures |
| ASI09 | Human-Agent Trust Exploitation |
| ASI10 | Rogue Agents |

Secondary sources also write the IDs with a year suffix, e.g. `ASI02:2026`.
