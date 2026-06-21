# Problem Set Progress Transfer Design

## Context

Problem set completion state is currently browser-local only. The detail page script `public/javascripts/problem-set-progress.js` reads and writes `localStorage` key `rbook.problem-set.progress`, with a simple object shape:

```json
{
  "luogu/P1001": true,
  "hdu/1213": true
}
```

This works for one browser, but users lose progress when changing computers or browsers. The feature should let users manually back up and restore this progress without adding accounts, a database, or server-side user state.

## Goals

- Add progress import and export controls on `/problem-sets`.
- Preserve the existing localStorage storage model and key.
- Let users transfer all problem-set progress between machines.
- Let users choose whether imported progress merges with or replaces current local progress.
- Keep the feature entirely client-side.

## Non-Goals

- No login, cloud sync, database, or server-side persistence.
- No per-problem-set progress files in the first version.
- No deletion of unknown problem keys during import.
- No changes to the problem-set Markdown format.

## User Experience

On the `/problem-sets` index page, place the controls near the existing title/meta area:

- `导入进度`
- `导出进度`
- A short status message area beside or below the buttons

The controls apply to all problem-set progress because the underlying storage key is global across problem sets.

Export downloads a JSON file, for example `rbook-progress.json`, and shows a status such as `已导出 128 条进度`.

Import flow:

1. User clicks `导入进度`.
2. Browser opens a file chooser for JSON files.
3. Script validates and normalizes the file.
4. User chooses one mode:
   - `合并`: imported completed keys are added to existing local progress.
   - `覆盖`: current local progress is replaced by the imported completed keys.
5. Script writes localStorage and shows a result such as `已合并导入 42 条进度` or `已覆盖导入 42 条进度`.

Import/export does not redirect the page. If the user is on `/problem-sets`, the visible list page stays in place.

## File Format

Use a versioned wrapper instead of exporting the raw storage object:

```json
{
  "type": "rbook.problem-set.progress",
  "version": 1,
  "exportedAt": "2026-06-21T00:00:00.000Z",
  "progress": {
    "luogu/P1001": true,
    "hdu/1213": true
  }
}
```

Validation rules:

- `type` must be `rbook.problem-set.progress`.
- `version` must be `1`.
- `progress` must be an object.
- Only entries whose value is exactly `true` are accepted.
- Unknown keys are preserved. They may correspond to old or future problem sets and have no harmful effect on current pages.

## Architecture

Add a dedicated front-end script for the index page, for example:

```text
public/javascripts/problem-set-progress-transfer.js
```

Keep the existing detail-page behavior in:

```text
public/javascripts/problem-set-progress.js
```

The new transfer script owns only index-page import/export UI. It should share the same localStorage key string and object semantics as the existing progress script, but avoid coupling to detail-page DOM nodes such as `[data-problem-task]`.

Update:

- `views/problem-sets-index.pug`: render import/export buttons, hidden file input, and status area.
- `public/javascripts/problem-set-progress-transfer.js`: implement read, write, export, import, validation, merge/overwrite, and status display.
- `tests/fastify-app.test.js`: assert the `/problem-sets` page includes the controls and script.

No API route is required.

## Error Handling

The import script should show a short status message for common failures:

- invalid JSON
- wrong `type`
- unsupported `version`
- missing or invalid `progress`
- localStorage write failure

The page should remain usable even if localStorage or file APIs fail.

## Testing

Add focused coverage for rendered HTML:

- `/problem-sets` includes `导入进度`, `导出进度`, the hidden file input, and the transfer script.

If the project later gets browser-level tests, add client-side behavior coverage for:

- export file shape
- merge import
- overwrite import
- ignoring non-`true` values
- preserving unknown keys
