import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

// TODO: In production, this should query a database or external API
// For now, we'll read from the existing project configurations
export async function GET() {
  try {
    // Read project configurations from the generated apps
    const projectsDir = join(process.cwd(), "..", "..", "generated-apps");
    
    // For now, return the known projects based on existing configurations
    // TODO: Implement dynamic project discovery from the filesystem
    const projects = [
      {
        id: "weight-tracker-nextjs",
        name: "Weight Tracker Pro",
        description: "AI-powered fitness tracking app with animated splash screens"
      },
      {
        id: "splendid-bdr",
        name: "Splendid BDR", 
        description: "Productivity app for business development representatives"
      }
    ];

    return NextResponse.json({ projects });
  } catch (error) {
    console.error("Error fetching projects:", error);
    return NextResponse.json(
      { error: "Failed to fetch projects" },
      { status: 500 }
    );
  }
}
