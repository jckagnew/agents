import Link from "next/link";
import { loadProjects } from "@/lib/data";

export default async function ProjectsPage() {
  const projects = await loadProjects();

  return (
    <div className="projects">
      <header>
        <h1>Projects</h1>
        <Link href="/projects/new" className="button">
          New project
        </Link>
      </header>

      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {projects.map((project) => (
            <tr key={project.id}>
              <td>
                <Link href={`/projects/${project.id}`}>{project.name}</Link>
              </td>
              <td>{project.description}</td>
              <td>
                <Link href={`/projects/${project.id}`} className="link">Edit</Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <style jsx>{`
        .projects {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
        }

        header {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        table {
          width: 100%;
          border-collapse: collapse;
          background: #ffffff;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 12px 24px rgba(15, 23, 42, 0.08);
        }

        th, td {
          padding: 1rem;
          text-align: left;
          border-bottom: 1px solid rgba(15, 23, 42, 0.06);
        }

        tr:last-child td {
          border-bottom: none;
        }

        .button {
          padding: 0.6rem 1.4rem;
          border-radius: 999px;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: white;
          text-decoration: none;
          font-weight: 600;
        }

        .link {
          color: #6366f1;
          text-decoration: none;
          font-weight: 600;
        }
      `}</style>
    </div>
  );
}
