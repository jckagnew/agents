import Link from "next/link";
import { loadProjects } from "@/lib/data";

async function loadHealthCount() {
  try {
    const res = await fetch("/api/health", { cache: "no-store" });
    if (!res.ok) return 0;
    const { alerts } = await res.json();
    return alerts?.length ?? 0;
  } catch {
    return 0;
  }
}

export default async function Dashboard() {
  const projects = await loadProjects();
  const healthCount = await loadHealthCount();

  return (
    <div className="dash">
      <h1>Factory Admin Overview</h1>
      <p>Manage projects, capabilities, and health signals across the software factory.</p>

      <div className="grid">
        <section className="card">
          <h2>Projects</h2>
          <p>{projects.length} active projects</p>
          <Link href="/projects" className="button">
            View projects
          </Link>
        </section>

        <section className="card">
          <h2>Health alerts</h2>
          <p>{healthCount} items under watch</p>
          <Link href="/health" className="button">
            View alerts
          </Link>
        </section>

        <section className="card">
          <h2>Splash Creator</h2>
          <p>Launch the interactive splash screen generator with project context.</p>
          <Link href="/splash" className="button">
            Open splash creator
          </Link>
        </section>
      </div>

      <style jsx>{`
        .dash {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }

        .grid {
          display: grid;
          gap: 1.5rem;
          grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
        }

        .card {
          background: #ffffff;
          padding: 1.5rem;
          border-radius: 18px;
          box-shadow: 0 18px 30px rgba(15, 23, 42, 0.08);
          display: flex;
          flex-direction: column;
          gap: 0.75rem;
        }

        .button {
          align-self: flex-start;
          padding: 0.6rem 1.4rem;
          border-radius: 999px;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: white;
          text-decoration: none;
          font-weight: 600;
        }
      `}</style>
    </div>
  );
}
