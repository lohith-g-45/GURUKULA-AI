
"use client";

import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { ErrorState } from "@/components/common/error-state";
import { AgentCard } from "@/components/common/AgentCard";
import { api } from "@/services/api";

export default function MonitoringPage() {
  const [isLoading, setIsLoading] = useState(false);

  const { data, error, isLoading: queryLoading, refetch } = useQuery({
    queryKey: ["agentStatus"],
    queryFn: async () => {
      const res = await api.agent.getStatus();
      return res.data;
    },
  });

  useEffect(() => {
    setIsLoading(queryLoading);
  }, [queryLoading]);

  if (isLoading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[60vh] gap-4">
        <Spinner size="lg" />
        <p className="text-gray-500 dark:text-gray-400">Loading agent status...</p>
      </div>
    );
  }

  if (error || !data?.success) {
    return (
      <ErrorState
        message="We couldn't retrieve the agent status. Please try again later."
        onRetry={() => refetch()}
      />
    );
  }

  const agents = data.data;

  return (
    <div className="container mx-auto p-4 md:p-6 lg:p-8">
      <PageHeader title="Agent Monitoring" description="Real-time status of all AI agents" />
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Total Agents</p>
            <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">
              {agents.length}
            </p>
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Active Agents</p>
            <p className="text-4xl font-bold text-green-600 dark:text-green-400">
              {agents.filter(a => a.status === "active").length}
            </p>
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Idle Agents</p>
            <p className="text-4xl font-bold text-yellow-600 dark:text-yellow-400">
              {agents.filter(a => a.status === "idle").length}
            </p>
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Average Success Rate</p>
            <p className="text-4xl font-bold text-purple-600 dark:text-purple-400">
              {Math.round(agents.reduce((acc, a) => acc + a.success_rate, 0) / agents.length)}%
            </p>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {agents.map((agent, idx) => (
          <AgentCard 
              key={idx} 
              name={agent.name} 
              status={agent.status as "active" | "idle" | "error"} 
              lastRun={agent.last_run} 
              successRate={agent.success_rate} 
            />
        ))}
      </div>
    </div>
  );
}
