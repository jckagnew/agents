"use client";

import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';

export default function HomePage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await fetch('/api/hello');
      if (!response.ok) throw new Error('Failed to fetch data');
      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8">
        {/* Header */}
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            🚀 {{PROJECT_NAME}}
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            {{PROJECT_DESCRIPTION}}
          </p>
          <Badge variant="outline" className="text-sm">
            Next.js {{NEXTJS_VERSION}} • TypeScript • Tailwind CSS
          </Badge>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {/* Feature Cards */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                ⚡ Fast Development
              </CardTitle>
              <CardDescription>
                Built with Next.js and Turbopack for lightning-fast development
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Hot reloading, TypeScript support, and optimized builds out of the box.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                🎨 Modern UI
              </CardTitle>
              <CardDescription>
                Beautiful components with Tailwind CSS and Radix UI
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                Responsive design with accessibility built-in.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                🔒 Secure
              </CardTitle>
              <CardDescription>
                Authentication and security best practices
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-gray-600">
                NextAuth.js integration with multiple providers.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* API Test Section */}
        <Card className="mb-8">
          <CardHeader>
            <CardTitle>API Test</CardTitle>
            <CardDescription>
              Test the API endpoint and see the response
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <Button 
                onClick={fetchData} 
                disabled={loading}
                className="w-full"
              >
                {loading ? 'Loading...' : 'Fetch Data'}
              </Button>
              
              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-md">
                  <p className="text-red-800">Error: {error}</p>
                </div>
              )}
              
              {data && (
                <div className="p-4 bg-green-50 border border-green-200 rounded-md">
                  <pre className="text-sm text-green-800">
                    {JSON.stringify(data, null, 2)}
                  </pre>
                </div>
              )}
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="text-center">
          <h2 className="text-2xl font-semibold text-gray-900 mb-4">
            Quick Actions
          </h2>
          <div className="flex flex-wrap justify-center gap-4">
            <Button variant="outline">
              📚 Documentation
            </Button>
            <Button variant="outline">
              🧪 Run Tests
            </Button>
            <Button variant="outline">
              🚀 Deploy
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}
