import { NextResponse } from "next/server";

const BACKEND_URL = "http://host.docker.internal:8000";

export async function POST(request: Request) {
  try {
    // 1. Get the form data from the Next.js client
    const incomingFormData = await request.formData();
    const file = incomingFormData.get("file") as File;
    const domainId = incomingFormData.get("domain_id") as string;

    if (!file || !domainId) {
      return NextResponse.json({ error: "Missing file or domain_id" }, { status: 400 });
    }

    // 2. Prepare the exact format the FastAPI backend expects
    const outgoingFormData = new FormData();
    outgoingFormData.append("domain_id", domainId);
    outgoingFormData.append("file", file);

    // 3. Forward to FastAPI
    const res = await fetch(`${BACKEND_URL}/summarize`, {
      method: "POST",
      body: outgoingFormData,
    });

    // 4. Handle backend errors gracefully
    if (!res.ok) {
      const errorText = await res.text();
      return NextResponse.json(
        { error: `Backend returned ${res.status}: ${errorText}` },
        { status: res.status }
      );
    }

    // 5. Return the successful response back to the browser
    const data = await res.json();
    return NextResponse.json(data);
  } catch (error: any) {
    console.error("Proxy error:", error);
    return NextResponse.json(
      { error: "Failed to communicate with the Python backend." },
      { status: 500 }
    );
  }
}