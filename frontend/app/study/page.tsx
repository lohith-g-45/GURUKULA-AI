"use client";

import { PageHeader } from "@/components/common/PageHeader";
import { AgentCard } from "@/components/common/AgentCard";
import { useHealth } from "@/hooks/use-health";
import {
  BookOpen,
  Calendar,
  RotateCcw,
  BrainCircuit,
  Sparkles,
} from "lucide-react";

export default function StudyPage() {
  const { data: healthData, isLoading, error } = useHealth();

  const agents = [
    {
      name: "Research Agent",
      description: "Gathers and analyzes study materials from various sources",
      icon: <BookOpen className="h-6 w-6" />,
    },
    {
      name: "Planning Agent",
      description: "Creates personalized study plans based on your goals",
      icon: <Calendar className="h-6 w-6" />,
    },
    {
      name: "Revision Agent",
      description: "Manages spaced repetition and revision scheduling",
      icon: <RotateCcw className="h-6 w-6" />,
    },
    {
      name: "Replanning Agent",
      description: "Adjusts study plans based on your progress",
      icon: <BrainCircuit className="h-6 w-6" />,
    },
    {
      name: "Insight Agent",
      description: "Provides data-driven insights into your learning patterns",
      icon: <Sparkles className="h-6 w-6" />,
    },
  ];

  return (
    <div className="p-8">
      <PageHeader
        title="Study Workspace"
        description="Study Workspace Coming Soon - AI-powered learning agents"
      />

      <div className="bg-card p-6 rounded-lg border mb-8">
        <div className="flex items-center gap-3 mb-2">
          <div
            className={`w-3 h-3 rounded-full ${
              isLoading
                ? "bg-yellow-500 animate-pulse"
                : error
                ? "bg-red-500"
                : healthData?.status === "healthy"
                ? "bg-green-500"
                : "bg-red-500"
            }`}
          />
          <span className="font-medium">Backend Connection Status</span>
        </div>
        <p className="text-muted-foreground">
          {isLoading
            ? "Checking..."
            : error
            ? "Disconnected"
            : healthData?.status === "healthy"
            ? "Connected and Healthy"
            : "Unknown Status"}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {agents.map((agent, index) => (
          <AgentCard
            key={index}
            name={agent.name}
            description={agent.description}
            status="idle"
            icon={agent.icon}
          />
        ))}
      </div>
    </div>
  );
}
