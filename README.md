# WheelHouse for GitHub Pages

Static wheelhouse project that publishes a PEP 503 `simple` index and wheel files via GitHub Pages.

## Layout

- `packages/`: wheel files (`*.whl`) tracked with Git LFS
- `simple/`: generated PEP 503 package index pages
- `scripts/sync_wheels.sh`: sync wheels from a local source directory
- `scripts/build_simple_index.py`: build `simple/` pages from `packages/`

## One-time setup

```bash
git init
git lfs install
git lfs track "*.whl"
git add .gitattributes
git commit -m "Initialize wheelhouse repository"
git branch -M main
```

Create a GitHub repo, add it as `origin`, and push:

```bash
git remote add origin <your-repo-url>
git push -u origin main
```

Enable GitHub Pages in repo settings (Source: GitHub Actions).

## Update wheelhouse content

Sync from your local wheel output directory:

```bash
./scripts/sync_wheels.sh /home/biali/Remoto/JETSON/delme/WheelBuilder/wheels packages
```

Generate the PEP 503 index:

```bash
python3 scripts/build_simple_index.py --packages-dir packages --simple-dir simple
```

Commit and push:

```bash
git add packages simple
git commit -m "Update wheelhouse packages and simple index"
git push
```

The workflow in `.github/workflows/pages.yml` deploys the repository to GitHub Pages.

## Pip install usage

Replace `<user>` and `<repo>`:

```bash
pip install <package-name> \
  --index-url https://<user>.github.io/<repo>/simple \
  --extra-index-url https://pypi.org/simple
```

For private or uncommon builds, pin an exact version where possible.

## Verify locally

Run the included test:

```bash
python3 -m unittest tests/test_build_simple_index.py
```

Optional quick smoke test for generated HTML links:

```bash
python3 scripts/build_simple_index.py --packages-dir packages --simple-dir simple
python3 -m http.server 8000
```

Then browse `http://localhost:8000/simple/`.

## Notes

- GitHub/LFS has storage and bandwidth quotas; monitor usage if your wheel set grows.
- Regenerate `simple/` every time `packages/` changes.
