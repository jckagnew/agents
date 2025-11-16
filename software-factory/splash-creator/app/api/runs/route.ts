import { NextResponse } from "next/server";
import { creativeBriefSchema } from "@/lib/schemas";
import { spawn } from "child_process";
import { writeFile, mkdir } from "fs/promises";
import { join } from "path";
import { randomUUID } from "crypto";

// TODO: In production, this should use a proper job queue system
// For now, we'll run the Python script directly
export async function POST(request: Request) {
  try {
    const payload = await request.json();
    const parsed = creativeBriefSchema.safeParse(payload);

    if (!parsed.success) {
      return NextResponse.json(
        { error: "Invalid creative brief", issues: parsed.error.issues },
        { status: 400 }
      );
    }

    const brief = parsed.data;
    const runId = randomUUID();
    
    // Create a temporary directory for this run
    const tempDir = join(process.cwd(), "..", "generated-apps", brief.projectId, "temp");
    await mkdir(tempDir, { recursive: true });
    
    // Write the brief to a temporary JSON file
    const briefPath = join(tempDir, `brief-${runId}.json`);
    await writeFile(briefPath, JSON.stringify(brief, null, 2));
    
    // Create a results file to track progress
    const resultsPath = join(tempDir, `results-${runId}.json`);
    const initialResults = {
      runId,
      status: "pending",
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      brief: brief,
      phases: {},
      artifacts: []
    };
    await writeFile(resultsPath, JSON.stringify(initialResults, null, 2));
    
    // Start the Python orchestration script
    const scriptPath = join(
      process.cwd(),
      "..",
      "generated-apps",
      brief.projectId,
      "scripts",
      "orchestrate-splash-creation.py"
    );
    
    console.log(`Running Python script: ${scriptPath}`);
    console.log(`Working directory: ${join(process.cwd(), "..", "generated-apps", brief.projectId, "scripts")}`);
    
    // Run the Python script in the background
    const pythonProcess = spawn("python3", [scriptPath], {
      cwd: join(process.cwd(), "..", "generated-apps", brief.projectId, "scripts"),
      stdio: ["pipe", "pipe", "pipe"]
    });
    
    // Handle process output and update results
    pythonProcess.stdout.on("data", (data) => {
      console.log(`Python stdout: ${data}`);
    });
    
    pythonProcess.stderr.on("data", (data) => {
      console.error(`Python stderr: ${data}`);
    });
    
    pythonProcess.on("close", async (code) => {
      try {
        // Read the workflow results
        const workflowResultsPath = join(
          process.cwd(),
          "..",
          "generated-apps", 
          brief.projectId,
          "scripts",
          "workflow_results.json"
        );
        
        let finalResults;
        try {
          const workflowContent = await import("fs/promises").then(fs => 
            fs.readFile(workflowResultsPath, "utf-8")
          );
          const workflowData = JSON.parse(workflowContent);
          
          // Transform workflow results to our format
          finalResults = {
            runId,
            status: code === 0 ? "complete" : "failed",
            createdAt: initialResults.createdAt,
            updatedAt: new Date().toISOString(),
            brief: brief,
            phases: workflowData.phases || {},
            artifacts: workflowData.final_prototypes?.map((prototype: any, index: number) => ({
              variantId: `variant-${index + 1}`,
              previewUrl: prototype.before_url || prototype.after_url,
              score: prototype.scores?.overall || 0,
              metadata: {
                rank: prototype.rank,
                beforeDescription: prototype.before_description,
                afterDescription: prototype.after_description,
                scores: prototype.scores,
                implementationSuggestions: prototype.implementation_suggestions
              }
            })) || [],
            error: code !== 0 ? `Process exited with code ${code}` : undefined
          };
        } catch (error) {
          finalResults = {
            ...initialResults,
            status: "failed",
            updatedAt: new Date().toISOString(),
            error: `Failed to read workflow results: ${error}`
          };
        }
        
        // Update the results file
        await writeFile(resultsPath, JSON.stringify(finalResults, null, 2));
        
        console.log(`Run ${runId} completed with status: ${finalResults.status}`);
      } catch (error) {
        console.error(`Error processing results for run ${runId}:`, error);
      }
    });
    
    // Return immediately with the run ID
    return NextResponse.json({
      runId,
      status: "pending",
      createdAt: initialResults.createdAt,
      updatedAt: initialResults.updatedAt
    }, { status: 202 });
    
  } catch (error) {
    console.error("Error submitting brief:", error);
    return NextResponse.json(
      { error: "Failed to submit brief" },
      { status: 500 }
    );
  }
}
