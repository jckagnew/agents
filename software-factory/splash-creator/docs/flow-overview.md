# Splash Creator Interactive Flow

## Step Overview

1. **Select Project**
   - Choose an existing factory project.
   - Loads design tokens (palette, typography, imagery cues) so the splash stays on-brand.
   - `Next` is disabled until a project is selected.

2. **Creative Brief**
   - Capture tone, headlines, CTA copy, audience, goals, and keyword hints.
   - Supports a custom tone option when "Other" is selected.
   - `Next` requires primary headline and CTA.

3. **Guidance Assets** (coming soon)
   - Placeholder for the upcoming uploader.
   - Will accept reference imagery, motion clips, and notes with priority tags.

4. **Review & Launch**
   - Summarises all selections, including keywords and guidance status.
   - Launches the workflow via `/api/runs` and surfaces run status.
   - Future iterations will add approval controls and variant preview cards.

## State Machine Sketch

```
project -> brief -> guidance -> review
   ^                         |
   |-------------------------|
```

- The `Back` button is always available (except on the first step) and returns to the previous state without clearing data.
- `Next` transitions only when the current step’s validation passes.
- Launching the workflow keeps the app on the review step; polling/approval UX will plug in here later.

## Data Responsibilities

- **Project step**
  - Fetch `/api/projects` -> list of `{ id, name }`.
  - Fetch `/api/projects/:id/design` to hydrate design tokens.
- **Brief step**
  - Maintain `FormState`; this is serialized into the `CreativeBrief` schema.
- **Guidance step**
  - Currently displays roadmap items. Once implemented, it will populate the `guidanceAssets` array in the brief.
- **Review step**
  - Builds the `CreativeBrief` payload and POSTs to `/api/runs`.
  - Displays workload status returned from the API.

## Planned Enhancements

- Drag-and-drop uploader with file validation and priority tagging.
- Human-in-the-loop approval before animation (pause/resume orchestration).
- Variant preview gallery with approve/reject/edit controls.
- Export options (download bundle, push to factory repo, register in admin).
