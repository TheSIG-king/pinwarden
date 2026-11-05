# Project name evaluation (checked 2026-11-05)

How we checked:
- **PyPI:** `https://pypi.org/pypi/<name>/json`. A 404 means the name is free. We did not check PyPI's similarity and typosquatting rules, which can still refuse a new name close to an existing one (UNVERIFIED for each candidate).
- **GitHub:** `https://api.github.com/search/repositories?q=<name>+in:name`.
- **npm:** `https://registry.npmjs.org/<name>`, as a bonus check.

These are all public read-only lookups. We did no trademark-office search: everything in the trademark column is a judgment call, not legal advice.

## Requested candidates

| Name | PyPI | npm | GitHub (`in:name`) | Conflicts / notes | Verdict |
|---|---|---|---|---|---|
| **mcpwarden** | free (404) | free | 6 repos, all 0★. Two are MCP auditors: [OneNobleSoul/mcpwarden](https://github.com/OneNobleSoul/mcpwarden) ("tool-definition rug-pull detection") and [rashedhasan090/mcpwarden](https://github.com/rashedhasan090/mcpwarden) | **Strong conflict.** PyPI already has two MCP security packages called `mcp-warden`: [mcp-warden](https://pypi.org/project/mcp-warden/) (raj8github, "MCP observability and control plane") and [mcp-warden-cli](https://pypi.org/project/mcp-warden-cli/) (a lockfile pinning and guard proxy, v2.2.0, 2026-10-24). That is a direct functional overlap. | Reject |
| **toolwarden** | **taken** ([PyPI](https://pypi.org/project/toolwarden/): "deterministic policy gate between an LLM agent and its tools", 2026-07) | free | 9 repos (0★) | Same concept, already published. | Reject |
| **mcp-sentry** | **taken** ([PyPI](https://pypi.org/project/mcp-sentry/): MCP server for Sentry.io issues) | – | 104 repos, many Sentry-integration MCP servers (e.g. [getsentry/sentry-mcp-stdio](https://github.com/getsentry/sentry-mcp-stdio)) | "Sentry" is Functional Software Inc.'s product brand, so trademark confusion is likely. | Reject |
| **mcplock** | **taken** ([PyPI](https://pypi.org/project/mcplock/): "Pin, diff, and lint MCP tool definitions", v1.0.3, 2026-07-29) | free | 10 repos (0–1★) | Same feature (pinning). | Reject |
| **tollgate-mcp** | free | **taken** ([npm](https://www.npmjs.com/package/tollgate-mcp): "Tollgate MCP marketplace — pay-per-call AI tools on Solana") | 0 exact. "tollgate" alone: 523 repos, e.g. [OpenTollGate/tollgate](https://github.com/OpenTollGate/tollgate) (62★) | In the MCP space "TollGate" already means pay-per-call (several x402 projects, e.g. [kravadk/TollGate](https://github.com/kravadk/TollGate)). The connotation is "payment", not "security". `mcp-tollgate` is free on PyPI, npm and GitHub. | Weak |
| **mcp-bastion** | free | **taken** (npm `mcp-bastion` exists) | 21 repos. Three are MCP security proxies: [cortex1020/McpBastion](https://github.com/cortex1020/McpBastion) (11★, "per-tool policy engine, argument inspection"), [Gowthaman90/mcp-bastion](https://github.com/Gowthaman90/mcp-bastion) (7★), [vaquarkhan/MCP-Bastion](https://github.com/vaquarkhan/MCP-Bastion) (7★) | Crowded with near-identical projects. Also "Azure Bastion" is a Microsoft product name. | Reject |

## Own proposals

| Name | PyPI | npm | GitHub (`in:name`) | Notes |
|---|---|---|---|---|
| **pinwarden** | free | free | 0 repos | No web hits for the exact string (search returned only "Penwarden" place names). It says exactly what the tool does: *pin* schemas plus *warden* for policy. It is close to the "warden" family, but there is no MCP-security project with this name. |
| **mcpgatekeeper** | free | free | 0 repos | Clear meaning. Risk of confusion with **OPA Gatekeeper** (CNCF policy project), so the generic word may be weak for search and SEO. |
| **mcp-tollgate** | free | free | 0 repos | Fixes the PyPI and npm collision of `tollgate-mcp`, but the MCP "TollGate" payments connotation remains. |
| *(also checked)* schemaward | free | – | 1 (SchemaWarden, 1★) | Fine, but less memorable. |
| *(also checked)* toolpin | free | – | 8 (unrelated, 0★) | Describes only pinning, not policy. |
| *(also checked)* mcpfence | free | – | `MCPFence` GitHub org exists (agent-security repos, up to 12★) | Reject: an org name collision in the same domain. |
| *(also checked)* mcp-pinwall | free | – | 0 | Okay. "pinwall" is otherwise a common word (44 repos). |

## Recommendation (top 3)

1. **pinwarden**. Free on PyPI, npm and GitHub; no web hits; no vendor trademark. It names the two headline features (full-schema **pin**ning plus a policy **warden**). The CLI reads well: `pinwarden run -- npx server`, `pinwarden lock`, `pinwarden diff`. Its one weakness is that it does not contain "mcp" for search; mitigate with GitHub topics and the PyPI summary "MCP security gateway".
2. **mcp-tollgate**. Free everywhere and easy to understand as a checkpoint metaphor. The downside is the existing MCP "TollGate" payment projects, which could cause confusion.
3. **mcpgatekeeper**. Free everywhere and explicit. The downsides are a generic word, OPA Gatekeeper association, and a long name.

None of the six names originally proposed is safe to adopt: five are already taken on PyPI or npm (toolwarden, mcp-sentry and mcplock on PyPI; tollgate-mcp and mcp-bastion on npm). The sixth, mcpwarden, is free on PyPI but sits next to two existing MCP-security `mcp-warden*` packages. **Decision belongs to the maintainer** (CLAUDE.md governance). Before final adoption: (a) do a quick EUIPO/USPTO trademark search, (b) register the PyPI name early, because availability can change at any time.
