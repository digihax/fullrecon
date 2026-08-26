# fullrecon

`fullrecon` is an OSCP-safe recon orchestrator for one or more explicit IPv4
targets. It wraps Nmap and local reporting helpers into a predictable phased
workflow: quick service discovery, web metadata/screenshots, then a heavier
single-target Nmap pass.

It is enumeration/documentation only:

- No exploitation
- No brute forcing
- No crawling, fuzzing, or directory busting
- No vulnerability scanners
- No Metasploit or Responder
- No hostnames or CIDR ranges

## Included Tools

- `fullrecon` - phased multi-target orchestrator
- `oscp-nmap-hard` - heavier single-target Nmap pass
- `oscp-nmap-summary` - parser for Nmap normal output
- `oscp-webshot` - web metadata and screenshot helper

## Install

Clone the repo and put the scripts on your PATH:

```bash
git clone https://github.com/digihax/fullrecon.git
cd fullrecon
chmod +x fullrecon oscp-nmap-hard oscp-nmap-summary oscp-webshot
sudo install -m 0755 fullrecon oscp-nmap-hard oscp-nmap-summary oscp-webshot /usr/local/bin/
```

Or run directly from the checkout:

```bash
./fullrecon 192.0.2.10
```

## Requirements

Required:

- Bash
- Python 3
- Nmap

Optional:

- Chromium or `wkhtmltoimage` for screenshots in `oscp-webshot`
- `scope_route_check.sh` for route-scope/LAN-leak guarding
- `oscp-service-triage`, `qnote`, and `qreport` if you use the broader OSCP
  artifact workflow

## Artifact Root

By default, output is written under:

```bash
/mnt/hgfs/_oscp_artifacts
```

Override that with:

```bash
export OSCP_ARTIFACTS=/path/to/artifacts
```

The expected output layout is:

```text
$OSCP_ARTIFACTS/
  runs/fullrecon_<timestamp>/
  targets/<ip>/
```

## Usage

```bash
fullrecon <ip> [ip...]
fullrecon -f ips.txt
fullrecon --phase1-only <ip>
fullrecon --no-hard <ip>
fullrecon --hard-only <ip>
fullrecon --web-only <ip>
fullrecon --resume <ip>
fullrecon --force <ip>
fullrecon --confirm-hard <ip>
fullrecon --allow-many <ip...>
fullrecon --allow-risk <ip>
```

Input files passed with `-f` may include comments and blank lines:

```text
# lab targets
192.0.2.10
192.0.2.11
```

## Phases

Phase 1 runs quick TCP service discovery:

```text
nmap -Pn --top-ports 100 -sV --version-light --reason
```

It also checks a small set of common OSCP challenge-lab odd ports, then writes
`phase1_open_tcp_ports.txt` and service summaries.

Phase 2 detects likely web services from Nmap output and captures metadata plus
screenshots when a supported screenshot backend is available. It does not crawl,
submit forms, fuzz paths, or dump source.

Phase 3 runs `oscp-nmap-hard` sequentially per target. That helper performs one
full TCP sweep when needed, then runs service/version/default-script coverage on
the discovered open TCP ports. UDP is limited to top 200 ports and only runs
when privileges allow it.

## Safety Controls

`fullrecon` rejects hostnames and CIDR ranges. It also limits larger target sets
unless `--allow-many` is supplied.

If `scope_route_check.sh` is installed, `fullrecon` runs it before scanning. A
failed route-scope check aborts the run unless you explicitly pass
`--allow-risk`.

The hard phase runs by default because the wrapper is designed as a complete
recon pass. Use `--confirm-hard` if you want an interactive gate before heavier
scans, or `--no-hard` to stop after quick and web phases.

## Generated Files

For each target, expect files similar to:

```text
targets/<ip>/00_phase1_top100_sV.nmap
targets/<ip>/00b_phase1_oddports.nmap
targets/<ip>/phase1_open_tcp_ports.txt
targets/<ip>/10_hard_tcp_services.nmap
targets/<ip>/12_hard_udp_top200.nmap
targets/<ip>/services_summary.txt
targets/<ip>/manual_next_checks.md
```

Each run also creates:

```text
runs/fullrecon_<timestamp>/fullrecon.log
runs/fullrecon_<timestamp>/run_summary.md
runs/fullrecon_<timestamp>/phase1_status.tsv
runs/fullrecon_<timestamp>/phase2_web_status.tsv
runs/fullrecon_<timestamp>/phase3_hard_status.tsv
```

## Helper Commands

Run the heavier scan for one target:

```bash
oscp-nmap-hard 192.0.2.10
```

Rebuild the Nmap service summary:

```bash
oscp-nmap-summary 192.0.2.10
oscp-nmap-summary 192.0.2.10 --only '00*.nmap' --out phase1_services_summary
```

Capture web metadata/screenshots:

```bash
oscp-webshot 192.0.2.10
```

## Notes

This tool records observations and creates operator checklists. It does not
decide exploitability, validate credentials, or perform attack traffic. Review
the generated summaries manually before taking action.

## License

MIT License. See `LICENSE`.
