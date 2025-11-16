import Link from "next/link";

export default function SplashIntegrationPage() {
  return (
    <div className="splash">
      <h1>Splash Creator Integration</h1>
      <p>
        Launch the interactive splash creator to configure animated splash screens. Select a project here,
        then open the creator to work with inherited design tokens and guidance inputs.
      </p>

      <ol>
        <li>Ensure the splash creator dev server is running (`npm run dev` in <code>splash-creator</code>).</li>
        <li>Open <Link href="http://localhost:3001" target="_blank">http://localhost:3001</Link> to access the interactive wizard.</li>
        <li>Use the project list below to copy IDs and context when launching runs.</li>
      </ol>

      <style jsx>{`
        .splash {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
          max-width: 720px;
        }

        ol {
          background: #ffffff;
          padding: 1.5rem;
          border-radius: 16px;
          box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        code {
          background: rgba(15, 23, 42, 0.08);
          padding: 0.15rem 0.35rem;
          border-radius: 6px;
        }
      `}</style>
    </div>
  );
}
