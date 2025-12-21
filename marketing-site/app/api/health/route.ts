import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json(
    { 
      status: 'healthy',
      timestamp: new Date().toISOString(),
      service: 'pinkflow-marketing-site',
      version: '0.1.0'
    },
    { status: 200 }
  )
}
