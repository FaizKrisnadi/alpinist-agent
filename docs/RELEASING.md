# Releasing

## Release Checklist

1. Ensure working tree is clean and CI is green on `main`.
2. Update version metadata:
   - `pyproject.toml`
   - `alpinist/__init__.py`
   - `CITATION.cff`
3. Update docs:
   - `CHANGELOG.md`
   - `RELEASE_NOTES_vX.Y.Z.md`
4. Run local checks:
   - `ruff check .`
   - `pytest`
   - `alpinist demo`
5. Push `main`:
   - `git push origin main`
6. Create annotated tag:
   - `git tag -a vX.Y.Z -m "vX.Y.Z: short summary"`
   - `git push origin vX.Y.Z`
7. Create GitHub Release from the tag and paste `RELEASE_NOTES_vX.Y.Z.md`.
8. If using Zenodo, follow `docs/ZENODO.md` and update citation DOI metadata.
