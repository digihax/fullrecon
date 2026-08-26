# fullrecon

OSCP-safe multi-target recon orchestration around Nmap and local reporting helpers.

`fullrecon` is enumeration/documentation only. It does not exploit, brute force,
crawl, fuzz, run vulnerability scanners, run Metasploit, use Responder, or make
decisions for the operator.

## Included tools

- `fullrecon` - phased multi-target orchestrator
- `oscp-nmap-hard` - heavier single-target Nmap pass
- `oscp-nmap-summary` - Nmap normal-output parser and service summary writer
- `oscp-webshot` - web service metadata and screenshot helper

## Usage

```bash
fullrecon <ip> [ip...]
fullrecon -f ips.txt
fullrecon --phase1-only <ip>
fullrecon --no-hard <ip>
fullrecon --hard-only <ip>
fullrecon --web-only <ip>
fullrecon --resume <ip>
```

By default, artifacts are written under:

```bash
/mnt/hgfs/_oscp_artifacts
```

Override that with:

```bash
export OSCP_ARTIFACTS=/path/to/artifacts
```

## Requirements

- Bash
- Python 3
- Nmap
- Optional: Chromium for screenshots via `oscp-webshot`

## Safety Notes

The wrapper rejects CIDR ranges and hostnames, limits broad target sets unless
explicitly overridden, and runs heavier scans sequentially. Review all output
manually before taking action.

