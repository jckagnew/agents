import { revalidatePath } from "next/cache";
import { notFound } from "next/navigation";
import { loadProjects, saveProjects } from "@/lib/data";
import type { FactoryProject } from "@/lib/types";

async function updateProject(projectId: string, formData: FormData) {
  "use server";

  const projects = await loadProjects();
  const index = projects.findIndex((project) => project.id === projectId);
  if (index === -1) {
    notFound();
  }

  const name = (formData.get("name") as string)?.trim();
  const description = (formData.get("description") as string)?.trim();
  const primaryColor = (formData.get("primaryColor") as string)?.trim();
  const headingFont = (formData.get("headingFont") as string)?.trim();

  const updated: FactoryProject = {
    ...projects[index],
    name: name || projects[index].name,
    description,
    designTokens: {
      ...projects[index].designTokens,
      palette: primaryColor
        ? [{ name: "Primary", value: primaryColor, role: "primary" }]
        : projects[index].designTokens?.palette,
      typography: headingFont
        ? [{ name: "Heading", fontFamily: headingFont, weight: 600 }]
        : projects[index].designTokens?.typography
    },
    updatedAt: new Date().toISOString()
  };

  projects[index] = updated;
  await saveProjects(projects);
  revalidatePath("/projects");
}

export default async function ProjectDetailPage({ params }: { params: { projectId: string } }) {
  const projects = await loadProjects();
  const project = projects.find((p) => p.id === params.projectId);

  if (!project) {
    notFound();
  }

  const primaryColor = project.designTokens?.palette?.[0]?.value ?? "";
  const headingFont = project.designTokens?.typography?.[0]?.fontFamily ?? "";

  async function action(formData: FormData) {
    "use server";
    await updateProject(params.projectId, formData);
  }

  return (
    <div className="project-detail">
      <header>
        <h1>{project.name}</h1>
        <p>{project.description}</p>
      </header>

      <form action={action} className="card">
        <h2>Design tokens</h2>
        <label>
          Primary color
          <input name="primaryColor" defaultValue={primaryColor} placeholder="#22c55e" />
        </label>
        <label>
          Heading font
          <input name="headingFont" defaultValue={headingFont} placeholder="Inter" />
        </label>
        <label>
          Description
          <textarea name="description" defaultValue={project.description ?? ""} />
        </label>
        <button type="submit">Save changes</button>
      </form>

      <style jsx>{`
        .project-detail {
          display: flex;
          flex-direction: column;
          gap: 1.75rem;
          max-width: 640px;
        }

        .card {
          display: flex;
          flex-direction: column;
          gap: 1rem;
          background: #ffffff;
          padding: 2rem;
          border-radius: 18px;
          box-shadow: 0 18px 30px rgba(15, 23, 42, 0.08);
        }

        label {
          display: flex;
          flex-direction: column;
          gap: 0.35rem;
          font-weight: 500;
        }

        input,
        textarea {
          padding: 0.65rem 0.75rem;
          border-radius: 0.75rem;
          border: 1px solid rgba(15, 23, 42, 0.12);
          font-size: 1rem;
        }

        button {
          align-self: flex-start;
          padding: 0.6rem 1.4rem;
          border-radius: 999px;
          border: none;
          background: linear-gradient(135deg, #6366f1, #a855f7);
          color: white;
          font-weight: 600;
          cursor: pointer;
        }
      `}</style>
    </div>
  );
}
