export function GuidancePlaceholder() {
  return (
    <div className="placeholder-card">
      <h3>Guidance uploader coming soon</h3>
      <p>
        Soon you’ll be able to drag-and-drop reference imagery, motion clips, and notes. The agent will
        prioritise uploads marked as “must use” and treat lower priority assets as inspiration only.
      </p>
      <ul>
        <li>Upload multiple assets with inline previews</li>
        <li>Tag assets with priority and usage notes</li>
        <li>Bias sourcing prompts with structured annotations</li>
        <li>Reuse saved guidance sets across projects</li>
      </ul>
      <p className="muted">For now, rely on tone, keywords, and project tokens to steer the workflow.</p>
      <style jsx>{`
        .placeholder-card {
          border: 1px dashed rgba(99, 102, 241, 0.4);
          border-radius: 12px;
          padding: 1.25rem;
          background: #f8faff;
        }

        ul {
          margin-top: 0.75rem;
          padding-left: 1.25rem;
        }

        li + li {
          margin-top: 0.35rem;
        }

        .muted {
          color: #475569;
        }
      `}</style>
    </div>
  );
}
