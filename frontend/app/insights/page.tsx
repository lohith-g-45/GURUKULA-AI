
"use client";

import { useState, useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { PageHeader } from "@/components/common/PageHeader";
import { Card } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { ErrorState } from "@/components/common/error-state";
import { ProgressBar } from "@/components/common/ProgressBar";
import { api } from "@/services/api";

export default function InsightsPage() {
  const [isLoading, setIsLoading] = useState(false);

  const { data, error, isLoading: queryLoading, refetch } = useQuery({
    queryKey: ["insights"],
    queryFn: async () => {
      const res = await api.agent.getInsights();
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
        <p className="text-gray-500 dark:text-gray-400">Loading insights...</p>
      </div>
    );
  }

  if (error || !data?.success) {
    return (
      <ErrorState
        message="We couldn't retrieve the insights. Please try again later."
        onRetry={() => refetch()}
      />
    );
  }

  const insights = data.data || {};
  const performance_summary = insights.performance_summary || {};
  const weak_subjects = insights.weak_subjects || [];
  const burnout_alerts = insights.burnout_alerts || [];
  const recommendations = insights.recommendations || [];
  const trends = insights.trends || {};
  const high_priority_subjects = trends.high_priority_subjects || [];
  const high_frequency_topics = trends.high_frequency_topics || [];

  return (
    <div className="container mx-auto p-4 md:p-6 lg:p-8">
      <PageHeader title="Insights" description="Personalized performance analytics" />
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Readiness Score</p>
            <div className="flex items-end gap-2">
              <p className="text-4xl font-bold text-blue-600 dark:text-blue-400">
                {performance_summary.current_readiness ?? 0}
              </p>
              <span className="text-sm text-gray-500 dark:text-gray-400 mb-1">/100</span>
            </div>
            <ProgressBar 
              value={performance_summary.current_readiness ?? 0} 
              max={100}
              color="blue"
            />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Tasks Completed</p>
            <p className="text-4xl font-bold text-green-600 dark:text-green-400">
              {performance_summary.completed_tasks ?? 0}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              of {performance_summary.total_tasks ?? 0} total
            </p>
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Completion Rate</p>
            <p className="text-4xl font-bold text-purple-600 dark:text-purple-400">
              {(performance_summary.completion_rate ?? 0).toFixed(0)}%
            </p>
            <ProgressBar 
              value={performance_summary.completion_rate ?? 0} 
              max={100}
              color="purple"
            />
          </div>
        </Card>
        
        <Card className="p-6">
          <div className="flex flex-col gap-2">
            <p className="text-sm text-gray-500 dark:text-gray-400">Study Streak</p>
            <p className="text-4xl font-bold text-orange-600 dark:text-orange-400">
              {performance_summary.study_streak ?? 0}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400">days</p>
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Weak Subjects</h3>
          <div className="space-y-4">
            {weak_subjects.map((subject, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-lg bg-gray-50 dark:bg-gray-800">
                <div>
                  <p className="font-medium">{subject.subject}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">
                    Weightage: {subject.weightage}% | Priority: {subject.priority}
                  </p>
                </div>
                <p className="text-xl font-bold text-red-500">{subject.score}</p>
              </div>
            ))}
          </div>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Burnout Alerts</h3>
          <div className="space-y-4">
            {burnout_alerts.length === 0 ? (
              <p className="text-sm text-gray-500 dark:text-gray-400">No burnout alerts</p>
            ) : (
              burnout_alerts.map((alert, idx) => (
                <div 
                  key={idx} 
                  className={`p-3 rounded-lg ${
                    alert.severity === "high" 
                      ? "bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800" 
                      : "bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800"
                  }`}
                >
                  <p className="font-medium capitalize">{alert.type}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{alert.message}</p>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Recommendations</h3>
          <div className="space-y-3">
            {recommendations.map((rec, idx) => (
              <div key={idx} className="flex gap-3 p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                <div className={`w-3 h-3 rounded-full mt-2 ${
                  rec.priority === "high" ? "bg-red-500" : 
                  rec.priority === "medium" ? "bg-yellow-500" : "bg-green-500"
                }`} />
                <div>
                  <p className="font-medium capitalize">{rec.type}</p>
                  <p className="text-sm text-gray-600 dark:text-gray-300">{rec.action}</p>
                </div>
              </div>
            ))}
          </div>
        </Card>
        
        <Card className="p-6">
          <h3 className="text-lg font-semibold mb-4">Trends</h3>
          <div className="space-y-4">
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">High Priority Subjects</p>
              <div className="flex flex-wrap gap-2">
                {high_priority_subjects.map((subject, idx) => (
                  <span 
                    key={idx} 
                    className="px-3 py-1 text-sm bg-blue-100 dark:bg-blue-800 text-blue-800 dark:text-blue-200 rounded-full"
                  >
                    {subject}
                  </span>
                ))}
              </div>
            </div>
            <div>
              <p className="text-sm text-gray-500 dark:text-gray-400 mb-2">High Frequency Topics</p>
              <div className="flex flex-wrap gap-2">
                {high_frequency_topics.slice(0, 10).map((topic, idx) => (
                  <span 
                    key={idx} 
                    className="px-3 py-1 text-sm bg-purple-100 dark:bg-purple-800 text-purple-800 dark:text-purple-200 rounded-full"
                  >
                    {topic}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </Card>
      </div>
    </div>
  );
}
