# Midnight Workshop

The owner selected the Midnight Workshop concept on 2026-11-16 and requested that it reflect their private repositories, with two named project families excluded. The repository mapping and exclusions remain in an ignored local configuration; only aggregate language data and edited portfolio summaries belong in the public profile source.

## Profile experience

An original animated SVG workshop cover introduces Santhosh and three areas of work: agentic systems, data protection, and developer tools. The warm amber and violet art remains legible as a static frame. Markdown supplies the biography, three substantial project summaries, a compact language table, and a short explanation that the underlying code is private. Additional work appears in an expandable section. No private repository links, raw repository names, unverified badges, invented metrics, or employer/customer details appear in the profile.

Use dark and light SVG variants selected with a picture element. Honor reduced motion within the SVG, leave a readable static scene as the base, and keep a pauseable/static option available via a normal Markdown link. Provide meaningful alt text and equivalent project/language text in Markdown. At narrow widths the artwork is decorative and its smaller text is not required to understand the profile. This is a GitHub README, not a custom JavaScript website. The standalone preview reproduces its assets and text for local review.

## Content and data

Read authorized private repository README files and language metadata using the saved Git credential. Filter the excluded project families before fetching contents or language information. Publication contains an explicit field selection: display name, handle, manually written biography, manually written project summaries, verified technology labels, aggregate language byte totals, repository sample count, and a retrieval date. Never copy repository README text, source files, configuration, credentials, commit messages, internal URLs, or individual repository activity into tracked output.

For statistics, use a local explicit repository allowlist drawn from the eligible private repositories. A denylist takes precedence. Exclude empty/data-only repositories, archived repositories, forks, and obvious backup snapshots. Describe language shares as GitHub-detected bytes across the sampled repositories, not personal proficiency, working hours, or a unique-code count. Similar code across repositories may be counted more than once. Missing access or a failed request aborts an update and preserves the last valid snapshot. A successful empty-language response is legitimate and does not count toward the language sample.

The checked-in sanitized snapshot is the input to a deterministic, standard-library Python renderer. The renderer has no authentication or network behavior. A separate opt-in local collector uses an ignored repository map and Git Credential Manager to fetch fresh language data; it writes an ignored candidate snapshot first. Reviewing and explicitly promoting that candidate updates the public snapshot. Existing output remains available if GitHub is down. Do not silently include newly created repositories.

## Scope and operations

The first version is a maintained snapshot, not a live dashboard. Its date is explicit. There is no scheduled private-data job and no broad personal token stored in GitHub Actions. The default GITHUB_TOKEN cannot read the owner's other private repositories. A manual local refresh is sufficient for the current scope; a scoped GitHub App or fine-grained token and an explicit disclosure process would be separate future work if requested.

The publishing destination is the authenticated account's standard profile repository, `SanthoshSamudrala009/SanthoshSamudrala009`. GitHub requires a public repository whose name matches the username to display the profile README. The owner's request includes a push; the account's repository inventory initially had no matching profile repository, so an empty profile repository is needed. Publish only the curated profile artifacts. Do not change visibility of any existing private source repository or overwrite an existing remote history.

## Acceptance

- The three main project summaries and technology choices are supported by the authorized source material and reveal only high-level capabilities.
- Both excluded project families contribute neither profile content nor language totals.
- Only the explicit public schema can enter the renderer; reject unknown keys, non-finite/negative counts, invalid identity values, and unsafe link/text inputs.
- The collector never executes repository content and never logs credentials or API payloads. It refuses partial updates.
- Refresh failures return a nonzero status with the failing stage and a safe error category, without private identifiers or API payloads. This incorporates the sole nit from seven completed EGM brainstorm reviews.
- Re-rendering an unchanged snapshot produces identical files; snapshots and dates are not fabricated.
- Parse all SVGs as XML and verify local image/link targets. View desktop and mobile previews in both themes. Exercise reduced motion and the static cover.
- Meaningful tests cover exclusion precedence, partial API failures, data validation, escaping, and rendering determinism.
- The commit contains only the profile, public snapshot, SVG assets, local preview, renderer/collector source, tests, and public maintenance documentation. Raw inventory, credentials, private mapping, research notes, review scratch files, and browser caches are ignored and absent from the commit.
