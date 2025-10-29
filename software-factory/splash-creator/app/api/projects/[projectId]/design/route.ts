import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

interface Params {
  params: { projectId: string };
}

// TODO: In production, this should query a design system database
// For now, we'll generate design tokens based on project type
export async function GET(_: Request, { params }: Params) {
  try {
    const { projectId } = params;
    
    // Try to read the project's splash config to get design information
    const configPath = join(
      process.cwd(), 
      "..", 
      "..", 
      "generated-apps", 
      projectId, 
      "splash-config.json"
    );
    
    let projectConfig;
    try {
      const configContent = await readFile(configPath, "utf-8");
      projectConfig = JSON.parse(configContent);
    } catch (error) {
      console.warn(`Could not read config for ${projectId}, using defaults`);
    }

    // Generate design tokens based on project type or config
    const designTokens = generateDesignTokens(projectId, projectConfig);
    
    return NextResponse.json({ designTokens });
  } catch (error) {
    console.error("Error fetching design tokens:", error);
    return NextResponse.json(
      { error: "Failed to fetch design tokens" },
      { status: 500 }
    );
  }
}

function generateDesignTokens(projectId: string, config?: any) {
  // Default design tokens based on project type
  const baseTokens = {
    palette: [
      { name: "Primary", value: "#22c55e", role: "primary" },
      { name: "Secondary", value: "#64748b", role: "secondary" },
      { name: "Accent", value: "#3b82f6", role: "accent" }
    ],
    typography: [
      { name: "Heading", fontFamily: "Nunito", weight: 700, size: "44px" },
      { name: "Body", fontFamily: "Inter", weight: 400, size: "16px" }
    ],
    components: [],
    imageryStyle: "Health and fitness lifestyle photography",
    animationStyle: "Smooth morphing gradients"
  };

  // Customize based on project type
  if (projectId === "splendid-bdr") {
    return {
      palette: [
        { name: "Primary", value: "#7c3aed", role: "primary" },
        { name: "Secondary", value: "#64748b", role: "secondary" },
        { name: "Accent", value: "#22d3ee", role: "accent" }
      ],
      typography: [
        { name: "Heading", fontFamily: "Poppins", weight: 600, size: "48px" },
        { name: "Body", fontFamily: "Inter", weight: 400, size: "18px" }
      ],
      components: [],
      imageryStyle: "High-energy go-to-market teams, collaborative workspace shots",
      animationStyle: "Slide-in panels with optimistic gradients"
    };
  }

  // Use config if available
  if (config) {
    const colorScheme = config.colorScheme || "red-to-green";
    const theme = config.theme || "transformation";
    
    // Map color schemes to actual colors
    const colorMap: Record<string, string[]> = {
      "red-to-green": ["#ef4444", "#22c55e"],
      "blue-to-gold": ["#3b82f6", "#f59e0b"],
      "purple-to-pink": ["#8b5cf6", "#ec4899"],
      "orange-to-yellow": ["#f97316", "#eab308"],
      "green-to-blue": ["#22c55e", "#3b82f6"],
      "purple-to-cyan": ["#8b5cf6", "#06b6d4"],
      "pink-to-purple": ["#ec4899", "#8b5cf6"]
    };

    const colors = colorMap[colorScheme] || colorMap["red-to-green"];
    
    return {
      ...baseTokens,
      palette: [
        { name: "Primary", value: colors[0], role: "primary" },
        { name: "Secondary", value: "#64748b", role: "secondary" },
        { name: "Accent", value: colors[1], role: "accent" }
      ],
      imageryStyle: `${theme} themed imagery`,
      animationStyle: `${config.animationType || "morphing"} animations`
    };
  }

  return baseTokens;
}
