# Post-Release DOI Checklist

Use this checklist after publishing release `v1.0.1`.

## 1. Enable Repository in Zenodo

1. Sign in to Zenodo.
2. Open GitHub integration settings.
3. Click **Sync now**.
4. Find `FaizKrisnadi/alpinist-agent` and toggle it **On**.

## 2. Confirm Release Archiving

1. `v1.0.1` is already released on GitHub.
2. In Zenodo, check whether a record/DOI was created for that release.
3. If not visible yet, use **Sync now** again and wait briefly.
4. If still missing, publish the next GitHub release (for example `v1.0.2`) to trigger DOI minting.

## 3. Apply DOI to Repository Metadata

After DOI is minted (example: `10.5281/zenodo.1234567`), update:

1. `CITATION.cff`: add DOI under `identifiers`.
2. `README.md`: add DOI badge near the top badges section.

Use this badge format in `README.md`:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.1234567.svg)](https://doi.org/10.5281/zenodo.1234567)
```

Replace the example DOI with your real DOI.

## 4. Use the Helper Script

Run:

```bash
# Example DOI argument; use your real DOI value.
bash scripts/set_doi.sh 10.5281/zenodo.1234567
```

The script will:

1. Update `CITATION.cff` DOI (`identifiers.value`).
2. Add or update the DOI badge in `README.md`.

The script fails if the DOI argument is missing or looks like a placeholder.
