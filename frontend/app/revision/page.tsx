"use client";

import { useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { RefreshCw, BookOpen, Lightbulb, Target, Calendar } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { PageHeader } from "@/components/common/PageHeader";
import { api } from "@/services/api";
import type { RevisionRequest } from "@/types/dashboard";
import { useToast } from "@/contexts/ToastContext";

export default function RevisionPage() {
  const { addToast } = useToast();
  const [subject, setSubject] = useState("");
  const [currentReadiness, setCurrentReadiness] = useState(70);
  const [revisionData, setRevisionData] = useState<Record<string, unknown> | null>(null);

  const mutation = useMutation({
    mutationFn: (data: RevisionRequest) => api.agent.getRevision(data),
    onSuccess: (res) => {
      setRevisionData(res.data.data);
      addToast("Revision schedule generated successfully!", "success");
    },
    onError: (err) => {
      console.error(err);
      addToast("Failed to generate revision schedule", "error");
    },
  });

  const handleGenerate = () => {
    mutation.mutate({
      subject: subject || undefined,
      current_readiness: currentReadiness,
    });
  };

  return (
    <div className="p-8">
      <div className="flex items-center justify-between mb-8">
        <PageHeader
          title="Revision Dashboard"
          description="Generate your revision schedule"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
        <Card>
          <CardContent className="p-6">
            <h3 className="font-semibold mb-4">Generate Revision Schedule</h3>
            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">Subject (optional)</label>
                <Input
                  placeholder="e.g., Polity"
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Current Readiness Score: {currentReadiness}%
                </label>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={currentReadiness}
                  onChange={(e) => setCurrentReadiness(parseInt(e.target.value))}
                  className="w-full"
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
                      <BookOpen className="h-4 w-4 mr-2" />
                      Generate Schedule
                    </>
                  )}
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {revisionData && (
        <div className="space-y-6">
          <h2 className="text-2xl font-bold">Revision Schedule</h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {Object.entries(revisionData).map(([key, value]) => (
              <Card key={key}>
                <CardHeader>
                  <CardTitle className="capitalize flex items-center gap-2">
                    {key.includes("schedule") || key.includes("plan") ? (
                      <Calendar className="h-5 w-5" />
                    ) : key.includes("priority") ? (
                      <Target className="h-5 w-5" />
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
