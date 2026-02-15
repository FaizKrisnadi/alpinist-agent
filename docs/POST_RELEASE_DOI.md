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

After DOI is minted (`10.5281/zenodo.XXXXXXX`), update:

1. `CITATION.cff`: add DOI under `identifiers`.
2. `README.md`: add DOI badge near the top badges section.

Use this badge format in `README.md`:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

Replace `10.5281/zenodo.XXXXXXX` with the real DOI.
