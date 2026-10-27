#!/usr/bin/env sh
# Render the article and publish the single self-contained page to the gh-pages
# branch, which GitHub Pages serves at manufacturinggenius.jarabana.com.
# Run from the project root after the checks pass. Pushes to origin.
set -eu

root=$(pwd)
python=${PYTHON:-.venv/Scripts/python.exe}
[ -x "$python" ] || python=.venv/bin/python
export QUARTO_PYTHON="$root/$python"

quarto render index.qmd

site=$(mktemp -d)
git worktree add --force "$site" gh-pages 2>/dev/null || {
  git worktree add --force --detach "$site"
  git -C "$site" checkout --orphan gh-pages
  git -C "$site" rm -rfq .
}
trap 'git worktree remove --force "$site"' EXIT

find "$site" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
cp _output/index.html "$site/index.html"
cp CNAME "$site/CNAME"
: > "$site/.nojekyll"

git -C "$site" add -A
if git -C "$site" diff --cached --quiet; then
  echo "gh-pages already matches the rendered article."
else
  git -C "$site" commit -q -m "Publish article from $(git rev-parse --short HEAD)"
fi
git -C "$site" push -q origin gh-pages
echo "Published gh-pages from $(git rev-parse --short HEAD)."
