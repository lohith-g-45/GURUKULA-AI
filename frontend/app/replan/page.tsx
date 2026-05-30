"use client";

import { useState } from "react";
import { useQuery, useMutation } from "@tanstack/react-query";
import { RefreshCw, TrendingUp, Calendar, AlertCircle, Lightbulb } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/common/PageHeader";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/common/error-state";
import { api } from "@/services/api";
import type { ReplanningRequest } from "@/types/dashboard";
import { useToast } from "@/contexts/ToastContext";

export default function ReplanPage() {
  const { addToast } = useToast();
  const [newAvailability, setNewAvailability] = useState<string>("");
  const [readinessChange, setReadinessChange] = useState<string>("");
  const [replanData, setReplanData] = useState<Record<string, unknown> | null>(null);

  const { data: tasks, isLoading, error, refetch } = useQuery({
    queryKey: ["tasks"],
    queryFn: async () => {
      const res = await api.tasks.get();
      return res.data.data;
    },
  });

  const mutation = useMutation({
    mutationFn: (data: ReplanningRequest) => api.agent.getReplan(data),
    onSuccess: (res) => {
      setReplanData(res.data.data);
      addToast("Replan generated successfully!", "success");
    },
    onError: (err) => {
      console.error(err);
      addToast("Failed to generate replan", "error");
    },
  });

  const handleGenerate = () => {
    mutation.mutate({
      current_tasks: tasks,
      new_availability: newAvailability ? parseFloat(newAvailability) : undefined,
      readiness_change: readinessChange ? parseFloat(readinessChange) : undefined,
    });
  };

  if (isLoading) {
    return (
      <div className="p-8">
        <PageHeader title="Replan Dashboard" description="Generate adaptive plans" />
        <Skeleton className="h-96" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-8">
        <ErrorState
          message="Failed to load tasks"
          onRetry={refetch}
        />
      </div>
    );
  }

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <PageHeader
          title="Replan Dashboard"
          description="Generate adaptive study plans"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold mb-4">Generate Replan</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">
                  New Availability (hours/day, optional)
                </label>
                <Input
                  type="number"
                  placeholder="e.g., 6"
                  value={newAvailability}
                  onChange={(e) => setNewAvailability(e.target.value)}
                  min={0}
                  step={0.5}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Readiness Change (optional)
                </label>
                <Input
                  type="number"
                  placeholder="e.g., -5"
                  value={readinessChange}
                  onChange={(e) => setReadinessChange(e.target.value)}
                />
              </div>
              <Button
                onClick={handleGenerate}
                disabled={mutation.isPending}
                className="w-full"
              >
                {mutation.isPending ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Generating...
                  </>
                ) : (
                    <>
                      <TrendingUp className="h-4 w-4 mr-2" />
                      Generate Replan
                    </>
                  )}
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="lg:col-span-2">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5" />
              Current Tasks ({tasks?.length || 0})
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3 max-h-80 overflow-y-auto">
              {tasks?.map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 border rounded-lg"
                >
                  <div>
                    <p className="font-medium">{task.title}</p>
                    <p className="text-sm text-muted-foreground">{task.subject}</p>
                  </div>
                  <span className="text-xs px-2 py-1 bg-secondary rounded-full capitalize">
                    {task.status.replace("_", " ")}
                  </span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {replanData && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Adaptive Plan</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(replanData).map(([key, value]) => (
              <Card key={key}>
                <CardHeader>
                  <CardTitle className="capitalize flex items-center gap-2">
                    {key.includes("recovery") || key.includes("suggestion") ? (
                      <AlertCircle className="h-5 w-5" />
                    ) : key.includes("schedule") ? (
                      <Calendar className="h-5 w-5" />
                    ) : (
                      <Lightbulb className="h-5 w-5" />
                    )}
                    {key.replace(/_/g, " ")}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  {typeof value === "object" && value !== null ? (
                    <pre className="text-sm whitespace-pre-wrap">
                      {JSON.stringify(value, null, 2)}
                    </pre>
                  ) : (
                      <p className="text-muted-foreground">{String(value ?? "")}</p>
                    )}
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
