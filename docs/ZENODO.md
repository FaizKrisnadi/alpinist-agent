# Zenodo DOI Setup

This project does not include a DOI yet. Use the steps below to mint one via Zenodo.

## 1. Connect GitHub Repository in Zenodo

1. Sign in to Zenodo.
2. Open the GitHub integration page.
3. Grant Zenodo access to your GitHub account if prompted.
4. Enable (toggle on) repository: `FaizKrisnadi/alpinist-agent`.

## 2. Create GitHub Release from `v1.0.0`

1. In GitHub, open the repository Releases page.
2. Click **Draft a new release**.
3. Select tag `v1.0.0`.
4. Title: `v1.0.0`.
5. Body: paste `RELEASE_NOTES_v1.0.0.md`.
6. Publish the release.

Zenodo will archive that release and mint a DOI.

## 3. Paste DOI into Citation Metadata

After Zenodo provides DOI `10.5281/zenodo.XXXXXXX`, update `CITATION.cff` with:

```yaml
identifiers:
  - type: doi
    value: 10.5281/zenodo.XXXXXXX
```

## 4. Add DOI Badge to README

After DOI is minted, add this badge near the top of `README.md`:

```markdown
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.XXXXXXX.svg)](https://doi.org/10.5281/zenodo.XXXXXXX)
```

Replace `10.5281/zenodo.XXXXXXX` with the real DOI.
