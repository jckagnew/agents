import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { loadProjects, saveProjects } from "@/lib/data";

async function createProject(formData: FormData) {
  "use server";

  const id = (formData.get("id") as string)?.trim();
  const name = (formData.get("name") as string)?.trim();
  const description = (formData.get("description") as string)?.trim();

  if (!id || !name) {
    throw new Error("Project ID and name are required");
  }

  const projects = await loadProjects();
  if (projects.some((project) => project.id === id)) {
    throw new Error("Project ID already exists");
  }

  const now = new Date().toISOString();
  projects.push({ id, name, description, createdAt: now, updatedAt: now });
  await saveProjects(projects);

  revalidatePath("/projects");
  redirect(`/projects/${id}`);
}

export default function NewProjectPage() {
  return (
    <div className="new-project">
      <h1>Create new project</h1>
      <form action={createProject}>
        <label>
          Project ID
          <input name="id" placeholder="weight-tracker-nextjs" required />
        </label>
        <label>
          Name
          <input name="name" placeholder="Weight Tracker" required />
        </label>
        <label>
          Description
          <textarea name="description" placeholder="One-line project overview" />
        </label>
        <button type="submit">Create project</button>
      </form>

      <style jsx>{`
        .new-project {
          display: flex;
          flex-direction: column;
          gap: 1.5rem;
          max-width: 480px;
        }

        form {
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
