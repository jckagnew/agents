import { NextResponse } from "next/server";
import { readFile, writeFile } from "fs/promises";
import { join } from "path";
import { glob } from "glob";

interface Params {
  params: { runId: string };
}

// TODO: In production, this should query a database
// For now, we'll read from the results files
export async function GET(_: Request, { params }: Params) {
  try {
    const { runId } = params;
    
    // Search for the results file across all projects
    const resultsPattern = join(
      process.cwd(),
      "..",
      "generated-apps",
      "**",
      "temp",
      `results-${runId}.json`
    );
    
    const resultsFiles = await glob(resultsPattern);
    
    if (resultsFiles.length === 0) {
      return NextResponse.json(
        { error: "Run not found" },
        { status: 404 }
      );
    }
    
    const resultsPath = resultsFiles[0];
    const resultsContent = await readFile(resultsPath, "utf-8");
    const results = JSON.parse(resultsContent);
    
    return NextResponse.json(results);
    
  } catch (error) {
    console.error("Error fetching run status:", error);
    return NextResponse.json(
      { error: "Failed to fetch run status" },
      { status: 500 }
    );
  }
}

export async function POST(request: Request, { params }: Params) {
  try {
    const { runId } = params;
    const body = await request.json().catch(() => ({} as any));
    const variantId = body?.variantId;

    if (typeof variantId !== "string" || !variantId) {
      return NextResponse.json({ error: "variantId required" }, { status: 400 });
    }

    // Search for the results file
    const resultsPattern = join(
      process.cwd(),
      "..",
      "generated-apps",
      "**",
      "temp",
      `results-${runId}.json`
    );
    
    const resultsFiles = await glob(resultsPattern);
    
    if (resultsFiles.length === 0) {
      return NextResponse.json(
        { error: "Run not found" },
        { status: 404 }
      );
    }
    
    const resultsPath = resultsFiles[0];
    const resultsContent = await readFile(resultsPath, "utf-8");
    const results = JSON.parse(resultsContent);
    
    // Mark the variant as approved
    if (results.artifacts) {
      const variant = results.artifacts.find((a: any) => a.variantId === variantId);
      if (variant) {
        variant.approved = true;
        variant.approvedAt = new Date().toISOString();
        
        // Update the results file
        results.updatedAt = new Date().toISOString();
        await writeFile(resultsPath, JSON.stringify(results, null, 2));
        
        console.log(`Variant ${variantId} approved for run ${runId}`);
      } else {
        return NextResponse.json(
          { error: "Variant not found" },
          { status: 404 }
        );
      }
    }
    
    return NextResponse.json({ ok: true });
    
  } catch (error) {
    console.error("Error approving variant:", error);
    return NextResponse.json(
      { error: "Failed to approve variant" },
      { status: 500 }
    );
  }
}
