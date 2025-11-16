import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";
import { healthAlertSchema } from "@/lib/schemas";

export async function GET() {
  try {
    const alertsPath = join(process.cwd(), "..", "data", "health-alerts.json");
    const raw = await readFile(alertsPath, "utf-8");
    const parsed = JSON.parse(raw);

    const alerts = Array.isArray(parsed)
      ? parsed
          .map((item) => {
            const result = healthAlertSchema.safeParse(item);
            return result.success ? result.data : null;
          })
          .filter(Boolean)
      : [];

    return NextResponse.json({ alerts });
  } catch (error) {
    console.error("Error reading health alerts", error);
    return NextResponse.json({ error: "Failed to load alerts" }, { status: 500 });
  }
}
