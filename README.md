# ProcessorCI Website

[![Pylint](https://github.com/LSC-Unicamp/processor-ci-website/actions/workflows/pylint.yml/badge.svg)](https://github.com/LSC-Unicamp/processor-ci-website/actions/workflows/pylint.yml)

ProcessorCI Website contains the public MkDocs documentation site for the
ProcessorCI project. It explains the suite, hardware infrastructure, supported
cores, software tests, contribution flow, and project overview pages.

## Repository Layout

```text
docs/                  MkDocs pages and assets
docs/assets/           Images and shared visual assets
data/                  Processor CSV inputs and generated Markdown tables
tools/                 Table, plotting, and Jenkins update utilities
scripts/               Compatibility wrappers for older utility paths
mkdocs.yml             Site configuration
requirements.txt       Documentation build dependencies
README.md              Repository landing page
```

## Installation

```bash
git clone https://github.com/LSC-Unicamp/processor-ci-website.git
cd processor-ci-website
python3 -m venv env
. env/bin/activate
pip install -r requirements.txt
```

## Quick Start

Serve the site locally:

```bash
mkdocs serve
```

Build the static site:

```bash
mkdocs build
```

Regenerate the processor table:

```bash
python tools/csv_to_md_table.py
```

The default input is `data/processadores.csv`, and the generated table is
written to `data/processors_table.md`.

Older commands under `scripts/` remain available as compatibility wrappers.

## Documentation Structure

Key pages live under `docs/`:

- `index.md` / `index.pt.md`: project landing pages.
- `about.md` / `about.pt.md`: suite overview.
- `hardware_infrastructure.md` / `.pt.md`: hardware and FPGA infrastructure.
- `software_tests.md` / `.pt.md`: software testing flow.
- `cores.md` / `.pt.md`: supported processor/core information.
- `contributing.md` / `.pt.md`: contribution guidance.

Keep English and Portuguese pages aligned when changing public-facing content.

## Development

Use this repository for website content and navigation only. Tool-specific
operational documentation should live in the corresponding ProcessorCI tool repo
and be linked from the website.

Website maintenance utilities live under `tools/`. Root-level
`update_pipelines.py` and scripts under `scripts/` are compatibility wrappers
for existing workflows.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). For content changes, include screenshots
or a short note describing the affected page.

## License

See [LICENSE](LICENSE).
