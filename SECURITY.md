# Security Policy

## Supported versions
The project is pre-1.0. Only the latest release on `main` receives security fixes.

## Reporting a vulnerability
Please **do not open a public issue** for security problems.

Use GitHub's private vulnerability reporting:
**Security → Advisories → Report a vulnerability** on this repository.

Include: affected version/commit, a minimal reproduction (ideally a local MCP server
and `policy.yaml`), observed vs expected behaviour, and impact.

We aim to acknowledge reports within 7 days and to agree on a disclosure timeline with
you (default: 90 days or on fix release, whichever comes first). Reporters are credited
unless they prefer otherwise.

## Scope
In scope: bypasses of pinning, detection or policy enforcement; secrets leaking into
audit logs; crashes or hangs triggered by a malicious MCP server or client message;
cases where the gateway fails open.

Out of scope: the threats listed under "Out of scope" in
[`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md), and vulnerabilities in third-party MCP
servers (report those to their maintainers).

## Testing ethics
This project's attack corpus and malicious test servers run **locally only**. Do not use
this project to scan or attack systems you do not own or are not authorized to test.
