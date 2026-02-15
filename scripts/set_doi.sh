#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: $0 <doi>"
  echo "Example: $0 10.5281/zenodo.1234567"
}

if [[ $# -ne 1 ]]; then
  usage
  exit 1
fi

doi="$1"
placeholder="10.5281/zenodo.XXXXXXX"

if [[ -z "${doi}" ]]; then
  echo "Error: DOI must not be empty."
  exit 1
fi

if [[ "${doi}" == "${placeholder}" || "${doi}" == *"XXXX"* || "${doi}" == *"xxxx"* ]]; then
  echo "Error: DOI looks like a placeholder: ${doi}"
  exit 1
fi

if [[ "${doi}" == *" "* ]]; then
  echo "Error: DOI must not contain spaces."
  exit 1
fi

if [[ ! "${doi}" =~ ^10\.[0-9]{4,9}/[-._;()/:A-Za-z0-9]+$ ]]; then
  echo "Error: DOI format is invalid: ${doi}"
  exit 1
fi

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
readme_file="${repo_root}/README.md"
citation_file="${repo_root}/CITATION.cff"

if [[ ! -f "${readme_file}" || ! -f "${citation_file}" ]]; then
  echo "Error: README.md and/or CITATION.cff not found."
  exit 1
fi

if ! grep -q "${placeholder}" "${readme_file}"; then
  echo "Error: README.md DOI placeholder not found (${placeholder})."
  exit 1
fi

if grep -q '^identifiers:[[:space:]]*$' "${citation_file}"; then
  if grep -q '^[[:space:]]*-[[:space:]]*type:[[:space:]]*doi[[:space:]]*$' "${citation_file}"; then
    DOI="${doi}" perl -0pi -e \
      's{(^\s*-\s*type:\s*doi\s*\n\s*value:\s*).*$}{$1$ENV{DOI}}m' "${citation_file}"
  else
    DOI="${doi}" perl -0pi -e \
      's{^(identifiers:\s*\n)}{$1  - type: doi\n    value: $ENV{DOI}\n}m' "${citation_file}"
  fi
else
  {
    echo
    echo "identifiers:"
    echo "  - type: doi"
    echo "    value: ${doi}"
  } >> "${citation_file}"
fi

DOI="${doi}" perl -0pi -e "s{\Q${placeholder}\E}{$ENV{DOI}}g" "${readme_file}"

echo "Updated DOI in:"
echo "- ${citation_file}"
echo "- ${readme_file}"
