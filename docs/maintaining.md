# Maintaining the workshop

The root README is the GitHub profile. `profile.json` contains its edited public text and a dated, aggregate language snapshot. The original cover illustration is in `templates/workshop.svg`. `scripts/visual_panels.py` draws the project illustrations, language gauges, tool pictograms, and experiment panel. Generated SVG variants are committed under `assets/` so they do not depend on a hosted statistics service.

The default profile is visual; its longer descriptions are in a collapsed text alternative. Each content panel has desktop/mobile and dark/light variants. Compact project titles and pictogram choices are presentation labels in `visual_panels.py`; update them when changing the three project themes. The mobile breakpoint is 600 pixels. `v1.0.0-midnight-workshop` preserves the original profile before this visual redesign.

## Edit and preview

Use Python 3.11 or newer. No packages need installing.

```powershell
python scripts/render_profile.py
python -m unittest discover -s tests -v
python scripts/render_profile.py --check
```

Open `preview/index.html` in a browser. It uses the actual generated artwork and content. Use its theme and static-artwork controls to inspect both variants. GitHub supplies its own typography and spacing when rendering `README.md`; the preview is not a promise of pixel-identical GitHub rendering.

## Refresh private-repository language totals

The ignored `profile.private.json` stores an explicit repository allowlist and exclusion patterns. On this workstation it has already been configured. It is deliberately absent from commits and must be recreated on another machine. Shape:

```json
{
  "owner": "YOUR-GITHUB-HANDLE",
  "repositories": ["a-repository-you-own"],
  "exclude": ["a-project-family-to-omit"]
}
```

Exclusions are compared case-insensitively after removing punctuation and spaces. They match substrings, so one family exclusion covers frontend/backend variants. Exclusions take precedence over the allowlist, before any per-repository request. Newly created repositories are never included automatically. The collector skips public, forked, archived, and empty-language repositories. It aborts on missing access or failed requests rather than publishing partial totals.

Sign in through Git Credential Manager, or provide a `PROFILE_READ_TOKEN` environment variable with read access to the selected repositories. Do not paste a token into a file or commit it. The repository language endpoint requires Metadata read permission for a fine-grained token. The collector only calls GitHub's repository metadata and language endpoints; it neither reads source files nor changes repositories.

```powershell
python scripts/collect_languages.py
git diff --no-index -- profile.json .preview-cache/profile.candidate.json
```

An exit code of 1 from `git diff --no-index` means that differences exist. Review the candidate date, sample count, and totals. The collector leaves `profile.json` and all published assets unchanged. After reviewing the candidate:

```powershell
Copy-Item -LiteralPath .preview-cache/profile.candidate.json -Destination profile.json
python scripts/render_profile.py
python -m unittest discover -s tests -v
```

Language shares are GitHub-detected bytes across the curated sample, not skill scores, time spent coding, unique source size, or contribution attribution. Related repositories can contain overlapping code. This profile does not claim badges or achievements that have not been verified.

## Publishing

GitHub displays a profile README from a **public** repository named exactly like the user's account. A private profile repository will not display it. Preserve any existing history before pushing to a destination. Never change the visibility of the private source repositories to make the profile work.

The public artifact consists of the edited snapshot, aggregate data, generated assets, templates, scripts, tests, and maintenance/design notes. `.preview-cache/`, `profile.private.json`, brainstorming notes, and the EGM scratch report stay local. Review `git diff --cached` before pushing. There is no scheduled workflow and no private-data token stored in GitHub Actions. Refreshes are manual and the date remains visible until the next one.

References: [profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme), [repository language endpoint](https://docs.github.com/en/rest/repos/repos#list-repository-languages), [workflow token access](https://docs.github.com/en/actions/concepts/security/github_token).
