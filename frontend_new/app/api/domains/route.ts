import { NextResponse } from "next/server";

// Using 127.0.0.1 is safer than localhost in Node.js to avoid IPv6 resolution issues
const BACKEND_URL = "http://127.0.0.1:8000";

export async function GET() {
  try {
    const res = await fetch(`${BACKEND_URL}/domains`, {
      cache: "no-store", // Ensure we get fresh data
    });

    if (!res.ok) throw new Error("Failed to fetch domains from backend");

    const data = await res.json();
    return NextResponse.json(data);
  } catch (error: any) {
    return NextResponse.json(
      { error: "Could not connect to the Python backend. Is it running?" },
      { status: 500 }
    );
  }
}