import { NextResponse } from "next/server";
import { loadProjects, saveProjects } from "@/lib/data";

interface Params {
  params: { projectId: string };
}

export async function GET(_: Request, { params }: Params) {
  const projects = await loadProjects();
  const project = projects.find((p) => p.id === params.projectId);
  if (!project) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }
  return NextResponse.json(project);
}

export async function PATCH(request: Request, { params }: Params) {
  const projects = await loadProjects();
  const index = projects.findIndex((p) => p.id === params.projectId);
  if (index === -1) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  const body = await request.json();
  const now = new Date().toISOString();
  projects[index] = {
    ...projects[index],
    ...body,
    updatedAt: now
  };

  await saveProjects(projects);
  return NextResponse.json(projects[index]);
}

export async function DELETE(_: Request, { params }: Params) {
  const projects = await loadProjects();
  const index = projects.findIndex((p) => p.id === params.projectId);
  if (index === -1) {
    return NextResponse.json({ error: "Not found" }, { status: 404 });
  }

  const [removed] = projects.splice(index, 1);
  await saveProjects(projects);
  return NextResponse.json(removed);
}
