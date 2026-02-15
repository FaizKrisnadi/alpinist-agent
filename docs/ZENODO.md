# Zenodo DOI Setup

This project does not include a DOI yet. After Zenodo is enabled for this repository, each new GitHub Release will be archived and assigned a DOI.

## 1. Connect GitHub Repository in Zenodo

1. Sign in to Zenodo.
2. Open the GitHub integration page.
3. Grant Zenodo access to your GitHub account if prompted.
4. Enable (toggle on) repository: `FaizKrisnadi/alpinist-agent`.

## 2. Create a GitHub Release (or Use Existing `v1.0.1`)

Option A (already prepared): use the existing `v1.0.1` release.

Option B (for future releases):

1. In GitHub, open the repository Releases page.
2. Click **Draft a new release**.
3. Select a new version tag (for example `v1.0.2`).
4. Add release title and notes.
5. Publish the release.

If Zenodo is enabled before release publication, DOI metadata is generated from that release.
If release already exists before Zenodo was enabled, use Zenodo **Sync now** and, if needed, publish the next release to trigger DOI minting.

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
