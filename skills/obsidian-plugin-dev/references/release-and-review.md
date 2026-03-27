# Release And Review

## Scope

Use this file when preparing a release, submitting to the community plugin list, or responding to review feedback.

## Pre-release checklist

- Repository root has:
  - `README.md`
  - `LICENSE`
  - `manifest.json`
- Manifest is ready:
  - version follows `x.y.z`
  - `minAppVersion` is appropriate
  - `description` is concise and formatted cleanly
- Build artifacts generated:
  - `main.js`
  - `manifest.json`
  - `styles.css` (optional)

## Create release

- Update `manifest.version`.
- Create Git tag equal to that version.
- Publish a GitHub release whose tag matches `manifest.version`.
- Upload required artifacts as binary attachments.

## Optional release automation

- Configure GitHub Actions to build and draft release on tag push.
- Ensure Actions permissions allow writing release contents.

## Submit to Obsidian community list

- Edit `obsidianmd/obsidian-releases` `community-plugins.json`.
- Add a new JSON entry with:
  - `id`
  - `name`
  - `author`
  - `description`
  - `repo` (`owner/repo`)
- Open PR with Community Plugin template and complete checklist.
- Wait for validation bot labels and resolve any validation failures.

## Review and resubmission behavior

- Address required reviewer changes in the same PR.
- Update release assets for new version when required.
- Comment on the same PR after fixes.
- Do not open a replacement PR for the same plugin submission.

## Common rejection/risk points

- Sample code or placeholder classes still present.
- Desktop-only APIs used without `isDesktopOnly: true`.
- Overlong or poorly formatted plugin description.
- Non-atomic file modification where conflicts are likely.
- Unsafe HTML insertion patterns.

## Source pages

- Plugins/Releasing/Submission requirements for plugins
- Plugins/Releasing/Submit your plugin
- Plugins/Releasing/Release your plugin with GitHub Actions
- Plugins/Releasing/Plugin guidelines
- Reference/Manifest
