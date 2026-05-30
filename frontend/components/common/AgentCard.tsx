import React from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Activity } from "lucide-react";

interface AgentCardProps {
  name: string;
  description?: string;
  status: "active" | "idle" | "error";
  lastRun?: string;
  successRate?: number;
  icon?: React.ReactNode;
}

export function AgentCard({ name, description, status, lastRun, successRate, icon }: AgentCardProps) {
  const statusColors = {
    active: "bg-green-500",
    idle: "bg-yellow-500",
    error: "bg-red-500",
  };

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardHeader className="flex flex-row items-center gap-4">
        <div className="p-3 rounded-full bg-primary/10 text-primary">
          {icon || <Activity className="h-6 w-6" />}
        </div>
        <div className="flex-1">
          <CardTitle className="text-lg">{name}</CardTitle>
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
        </div>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${statusColors[status]}`} />
          <span className="text-xs text-muted-foreground capitalize">
            {status}
          </span>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-2">
          {lastRun && (
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Last Run</span>
              <span className="text-sm font-medium">{lastRun}</span>
            </div>
          )}
          {successRate !== undefined && (
            <div className="flex justify-between">
              <span className="text-sm text-muted-foreground">Success Rate</span>
              <span className="text-sm font-medium">{successRate}%</span>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
