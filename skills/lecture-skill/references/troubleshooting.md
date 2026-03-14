# Troubleshooting

## 1) `unrecognized arguments: --target claude`

Cause:
- You passed `--target` to `create`.

Fix:
```bash
skill-seekers create <source>
skill-seekers package output/<skill-name> --target claude
```

## 2) `Found 0 source files`

Cause:
- You used `create ./folder` on a PDF-only folder.

Fix:
- Use unified config with `sources` and `type: "pdf"`.
- Or run `skill-seekers pdf --pdf <file>`.

## 3) Unified output index has no lecture markdown links

Cause:
- Old `skill-seekers` build without PDF reference aggregation patch.

Fix:
- Install patched build.
- Re-run:
```bash
skill-seekers unified --config arch-config.json
```
- Check:
`output/<skill-name>/references/pdf/index.md`

## 4) Want to keep per-lecture intermediates for debugging

Default:
- Intermediates are cleaned after unified build.

Fix:
```bash
skill-seekers unified --config arch-config.json --keep-pdf-intermediates
```

## 5) Config schema errors

Checklist:
- top-level has `name`, `description`, `sources`.
- `sources` must be a non-empty array.
- each PDF source needs:
```json
{ "type": "pdf", "path": "relative/or/absolute/path.pdf" }
```
