"use client";

import type { DesignTokens } from "@/lib/schemas";

interface Props {
  tokens: DesignTokens | null;
  projectName?: string;
  isLoading?: boolean;
}

export function DesignTokenPreview({ tokens, projectName, isLoading }: Props) {
  if (isLoading) {
    return <section className="panel">Loading design tokens…</section>;
  }

  if (!tokens) {
    return (
      <section className="panel">
        <p>Select a project to inherit its design language.</p>
      </section>
    );
  }

  return (
    <section className="panel">
      <h2 style={{ marginTop: 0 }}>
        Design DNA {projectName ? `· ${projectName}` : ""}
      </h2>

      {tokens.palette.length > 0 && (
        <div className="token-group">
          <h3>Palette</h3>
          <div className="swatch-row">
            {tokens.palette.map((color) => (
              <div key={color.name} className="swatch">
                <div
                  className="swatch-color"
                  style={{ backgroundColor: color.value }}
                />
                <span className="swatch-name">{color.name}</span>
                <span className="swatch-value">{color.value}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {tokens.typography.length > 0 && (
        <div className="token-group">
          <h3>Typography</h3>
          <ul className="typo-list">
            {tokens.typography.map((typo) => (
              <li key={typo.name}>
                <strong>{typo.name}</strong> · {typo.fontFamily}
                {typo.size ? ` · ${typo.size}` : ""}{" "}
                {typo.weight ? ` · ${typo.weight}` : ""}
              </li>
            ))}
          </ul>
        </div>
      )}

      {(tokens.imageryStyle || tokens.animationStyle) && (
        <div className="token-group">
          {tokens.imageryStyle && (
            <p>
              <strong>Imagery:</strong> {tokens.imageryStyle}
            </p>
          )}
          {tokens.animationStyle && (
            <p>
              <strong>Animation:</strong> {tokens.animationStyle}
            </p>
          )}
        </div>
      )}

      <style jsx>{`
        .panel {
          padding: 1.5rem;
          background: #ffffff;
          border-radius: 16px;
          box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }

        .token-group:not(:last-child) {
          margin-bottom: 1.5rem;
        }

        .swatch-row {
          display: flex;
          flex-wrap: wrap;
          gap: 1rem;
        }

        .swatch {
          width: 120px;
          border-radius: 12px;
          overflow: hidden;
          border: 1px solid rgba(15, 23, 42, 0.08);
          background: #f8fafc;
          font-size: 0.8rem;
          text-align: center;
        }

        .swatch-color {
          height: 60px;
        }

        .swatch-name {
          display: block;
          font-weight: 600;
          padding-top: 0.5rem;
        }

        .swatch-value {
          display: block;
          padding: 0 0 0.75rem;
          color: #475569;
        }

        .typo-list {
          padding-left: 1.25rem;
          margin: 0;
          display: flex;
          flex-direction: column;
          gap: 0.5rem;
        }
      `}</style>
    </section>
  );
}
