import Link from "next/link";
import { readFile } from "fs/promises";
import { join } from "path";

async function loadAlerts() {
  const alertsPath = join(process.cwd(), "..", "data", "health-alerts.json");
  const raw = await readFile(alertsPath, "utf-8");
  return JSON.parse(raw) as Array<{
    id: string;
    title: string;
    severity: string;
    status: string;
    updatedAt?: string;
    references?: string[];
  }>;
}

export default async function HealthPage() {
  const alerts = await loadAlerts();

  return (
    <div className="health">
      <h1>Health alerts</h1>
      <p>Track dependency issues, external risks, and follow-up dates.</p>

      <div className="list">
        {alerts.map((alert) => (
          <article key={alert.id} className="alert">
            <header>
              <span className={`severity severity--${alert.severity}`}>{alert.severity}</span>
              <h2>{alert.title}</h2>
            </header>
            <p>Status: <strong>{alert.status}</strong></p>
            {alert.updatedAt && <p>Updated: {new Date(alert.updatedAt).toLocaleString()}</p>}
            {alert.references && alert.references.length > 0 && (
              <ul>
                {alert.references.map((ref) => (
                  <li key={ref}>
                    <Link href={ref}>{ref}</Link>
                  </li>
                ))}
              </ul>
            )}
          </article>
        ))}
      </div>

      <style jsx>{`
        .health {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        .list {
          display: grid;
          gap: 1.25rem;
        }

        .alert {
          padding: 1.5rem;
          background: #ffffff;
          border-radius: 16px;
          box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }

        header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }

        .severity {
          padding: 0.25rem 0.75rem;
          border-radius: 999px;
          font-size: 0.75rem;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .severity--critical {
          background: rgba(220, 38, 38, 0.15);
          color: #b91c1c;
        }

        .severity--high {
          background: rgba(245, 158, 11, 0.15);
          color: #b45309;
        }

        .severity--medium {
          background: rgba(59, 130, 246, 0.15);
          color: #1d4ed8;
        }

        .severity--low {
          background: rgba(34, 197, 94, 0.15);
          color: #15803d;
        }

        ul {
          margin-top: 0.5rem;
          padding-left: 1.25rem;
        }
      `}</style>
    </div>
  );
}
