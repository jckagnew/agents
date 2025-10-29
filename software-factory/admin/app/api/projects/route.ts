import { NextResponse } from "next/server";
import { loadProjects, saveProjects } from "@/lib/data";
import type { FactoryProject } from "@/lib/types";

export async function GET() {
  const projects = await loadProjects();
  return NextResponse.json({ projects });
}

export async function POST(request: Request) {
  const body = await request.json();
  if (!body?.id || !body?.name) {
    return NextResponse.json({ error: "id and name required" }, { status: 400 });
  }

  const projects = await loadProjects();
  if (projects.some((project) => project.id === body.id)) {
    return NextResponse.json({ error: "Project ID already exists" }, { status: 409 });
  }

  const now = new Date().toISOString();
  const newProject: FactoryProject = {
    ...body,
    createdAt: now,
    updatedAt: now
  };

  projects.push(newProject);
  await saveProjects(projects);

  return NextResponse.json(newProject, { status: 201 });
}
