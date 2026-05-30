"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useHealth } from "@/hooks/use-health";
import { useDashboard } from "@/hooks/use-dashboard";
import { useTheme } from "@/contexts/theme-context";
import { env } from "@/utils/env";

export default function DebugPage() {
  const { theme } = useTheme();
  const healthQuery = useHealth();
  const dashboardQuery = useDashboard();
  const [showErrors, setShowErrors] = useState(false);

  const throwError = () => {
    throw new Error("Intentional error for testing!");
  };

  return (
    <div className="p-8 space-y-6">
      <h1 className="text-3xl font-bold">Debug Information</h1>

      <Card>
        <CardHeader>
          <CardTitle>Environment</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="text-sm bg-muted p-4 rounded-lg overflow-auto">
            {JSON.stringify(
              {
                NEXT_PUBLIC_API_URL: env.NEXT_PUBLIC_API_URL,
              },
              null,
              2
            )}
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Theme</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-muted-foreground">Current theme: {theme}</p>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Health Check</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="text-sm bg-muted p-4 rounded-lg overflow-auto">
            {JSON.stringify(
              {
                isLoading: healthQuery.isLoading,
                error: showErrors ? healthQuery.error?.message : "hidden",
                data: healthQuery.data,
              },
              null,
              2
            )}
          </pre>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Dashboard Query</CardTitle>
        </CardHeader>
        <CardContent>
          <pre className="text-sm bg-muted p-4 rounded-lg overflow-auto">
            {JSON.stringify(
              {
                isLoading: dashboardQuery.isLoading,
                error: showErrors ? dashboardQuery.error?.message : "hidden",
                data: dashboardQuery.data,
              },
              null,
              2
            )}
          </pre>
        </CardContent>
      </Card>

      <div className="space-x-4">
        <Button onClick={() => healthQuery.refetch()}>Refetch Health</Button>
        <Button onClick={() => dashboardQuery.refetch()}>Refetch Dashboard</Button>
        <Button variant="destructive" onClick={throwError}>
          Throw Error
        </Button>
        <Button variant="outline" onClick={() => setShowErrors(!showErrors)}>
          {showErrors ? "Hide Errors" : "Show Errors"}
        </Button>
      </div>
    </div>
  );
}
