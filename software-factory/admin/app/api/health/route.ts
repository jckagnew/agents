import { NextResponse } from "next/server";
import { readFile } from "fs/promises";
import { join } from "path";

export async function GET() {
  try {
    const alertsPath = join(process.cwd(), "..", "data", "health-alerts.json");
    const raw = await readFile(alertsPath, "utf-8");
    const parsed = JSON.parse(raw);
    return NextResponse.json({ alerts: parsed });
  } catch (error) {
    console.error("Health alert read error", error);
    return NextResponse.json({ alerts: [] });
  }
}
