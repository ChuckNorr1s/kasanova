// src/app/api/stream/route.ts
import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export const maxDuration = 300; // This function can run for a maximum of 300 seconds

export async function GET(request: Request) {
  // Parse query parameters from the request URL.
  const { searchParams } = new URL(request.url);
  const query = searchParams.get('query') || 'What is the meaning of life?';
  const doctrine = searchParams.get('doctrine') || 'Reinvest for Revolution!';
  const toxicity = searchParams.get('toxicity') || '2.0';

  // added a fixing comment
  // Build the URL for your FastAPI streaming endpoint.
  const fastApiUrl = `https://sabotage.hoshi-ai.com/stream?query=${encodeURIComponent(
    query
  )}&doctrine=${encodeURIComponent(doctrine)}&toxicity=${toxicity}`;

  try {
    // Call the FastAPI streaming endpoint.
    const response = await fetch(fastApiUrl);

    if (!response.ok) {
      return NextResponse.json(
        { error: 'Error fetching stream from FastAPI.' },
        { status: response.status }
      );
    }

    // The FastAPI endpoint returns a ReadableStream.
    const stream = response.body;
    // fix username
    // Return a streaming response to the client.
    return new Response(stream, {
      headers: {
        'Content-Type': 'text/plain; charset=utf-8',
        'Cache-Control': 'no-cache',
        'Transfer-Encoding': 'chunked',
         Connection: 'keep-alive',
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'Internal server error.' },
      { status: 500 }
    );
  }
}
