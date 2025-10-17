import { NextRequest, NextResponse } from 'next/server';

export async function GET(request: NextRequest) {
  try {
    // Get query parameters
    const { searchParams } = new URL(request.url);
    const name = searchParams.get('name') || 'World';
    
    // Simulate some processing
    const timestamp = new Date().toISOString();
    const randomId = Math.random().toString(36).substring(7);
    
    const response = {
      message: `Hello, ${name}!`,
      timestamp,
      id: randomId,
      status: 'success',
      data: {
        environment: process.env.NODE_ENV,
        version: '1.0.0',
        features: [
          'Next.js 15',
          'TypeScript',
          'Tailwind CSS',
          'Radix UI',
          'NextAuth.js',
          'Supabase'
        ]
      }
    };
    
    return NextResponse.json(response, {
      status: 200,
      headers: {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0',
      },
    });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal Server Error',
        message: 'Something went wrong',
        status: 'error'
      },
      { status: 500 }
    );
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    
    // Validate request body
    if (!body.name) {
      return NextResponse.json(
        { 
          error: 'Validation Error',
          message: 'Name is required',
          status: 'error'
        },
        { status: 400 }
      );
    }
    
    // Process the request
    const response = {
      message: `Hello, ${body.name}!`,
      timestamp: new Date().toISOString(),
      receivedData: body,
      status: 'success'
    };
    
    return NextResponse.json(response, { status: 201 });
  } catch (error) {
    console.error('API Error:', error);
    return NextResponse.json(
      { 
        error: 'Internal Server Error',
        message: 'Failed to process request',
        status: 'error'
      },
      { status: 500 }
    );
  }
}
