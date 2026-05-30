"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useDashboard } from "@/hooks/use-dashboard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/common/error-state";
import { PageHeader } from "@/components/common/PageHeader";
import { StatCard } from "@/components/common/StatCard";
import { ProgressBar } from "@/components/common/ProgressBar";
import {
  CheckCircle,
  Target,
  BookOpen,
  TrendingUp,
  AlertTriangle,
  Lightbulb,
  Star,
  ShieldAlert,
} from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";

export default function Home() {
  const router = useRouter();
  const { profile, isLoading: profileLoading } = useUserProfile();
  const { data, isLoading, error, refetch } = useDashboard();

  useEffect(() => {
    if (!profileLoading && !profile) {
      router.push("/onboarding");
    }
  }, [profile, profileLoading, router]);

  if (profileLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <Skeleton className="h-8 w-32" />
      </div>
    );
  }

  if (!profile) {
    return null;
  }

  if (isLoading) {
    return (
      <div className="p-8">
        <PageHeader title="Dashboard" description="Your learning overview" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <Skeleton className="h-96" />
          <Skeleton className="h-96" />
        </div>
      </div>
    );
  }

  if (error) {
    const errorMessage =
      error instanceof Error ? error.message : "Failed to load dashboard";
    return (
      <div className="p-8">
        <ErrorState message={errorMessage} onRetry={refetch} />
      </div>
    );
  }

  if (!data) {
    return null;
  }

  const { research, studentAnalysis } = data;

  // Default values if fields are missing
  const readinessScore = studentAnalysis?.readiness_score ?? 70;
  const highPrioritySubjects = research?.research_summary?.high_priority_subjects ?? [];
  const strengths = studentAnalysis?.strengths ?? [];
  const weaknesses = studentAnalysis?.weaknesses ?? [];
  const recommendations = studentAnalysis?.recommendations ?? [];
  const riskIndicators = studentAnalysis?.risk_indicators ?? [];
  const frequentTopics = research?.research_summary?.frequent_topics ?? [];
  const actionableInsights = research?.actionable_insights ?? [];
  const examOverview = research?.research_summary?.exam_overview ?? "Karnataka Administrative Service (KAS) exam preparation overview";
  const metadata = research?.metadata ?? {
    conducted_by: "KPSC",
    stages: ["Prelims", "Mains", "Interview"],
    qualification: "Bachelor's Degree",
    difficulty: "High"
  };

  return (
    <div className="p-8">
      <PageHeader title="Dashboard" description="Your learning overview" />

      {/* Top Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <StatCard
          title="Readiness Score"
          value={`${readinessScore}%`}
          icon={<Target className="h-6 w-6" />}
        />
        <StatCard
          title="High Priority Subjects"
          value={highPrioritySubjects.length}
          icon={<BookOpen className="h-6 w-6" />}
        />
        <StatCard
          title="Strengths"
          value={strengths.length}
          icon={<Star className="h-6 w-6 text-yellow-500" />}
        />
        <StatCard
          title="Weaknesses"
          value={weaknesses.length}
          icon={<TrendingUp className="h-6 w-6 text-orange-500" />}
        />
      </div>

      {/* Research Insights Section */}
      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <BookOpen className="h-6 w-6" />
          Research Insights
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Exam Overview */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Exam Overview</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <p className="text-muted-foreground">
                {examOverview}
              </p>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <p className="text-sm text-muted-foreground">Conducted By</p>
                  <p className="font-medium">{metadata.conducted_by}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Difficulty</p>
                  <p className="font-medium">{metadata.difficulty}</p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Stages</p>
                  <p className="font-medium">
                    {(metadata.stages ?? []).join(", ")}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-muted-foreground">Qualification</p>
                  <p className="font-medium">{metadata.qualification}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Priority Subjects */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">High Priority Subjects</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex flex-wrap gap-2">
                {highPrioritySubjects.map(
                  (subject, i) => (
                    <span
                      key={i}
                      className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
                    >
                      {subject}
                    </span>
                  )
                )}
              </div>
            </CardContent>
          </Card>

          {/* Frequent Topics */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Frequent Topics</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2">
                {frequentTopics.map((topic, i) => (
                  <div
                    key={i}
                    className="flex items-center justify-between"
                  >
                    <span className="font-medium">{topic.topic}</span>
                    <span className="text-sm text-muted-foreground">
                      {topic.frequency} occurrences
                    </span>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Actionable Insights */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                Actionable Insights
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2">
                {actionableInsights.map((insight, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <CheckCircle className="h-5 w-5 text-green-500 mt-0.5 flex-shrink-0" />
                    <span>{insight}</span>
                  </li>
                ))}
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Student Analysis Section */}
      <div>
        <h2 className="text-2xl font-bold mb-4 flex items-center gap-2">
          <Target className="h-6 w-6" />
          Student Analysis
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Readiness Score */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg">Readiness Score</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center mb-4">
                <p className="text-5xl font-bold text-blue-600">
                  {readinessScore}%
                </p>
              </div>
              <ProgressBar
                value={readinessScore}
                max={100}
              />
            </CardContent>
          </Card>

          {/* Strengths */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Star className="h-5 w-5 text-yellow-500" />
                Strengths
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {strengths.map((item, i) => (
                  <div key={i} className="border rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium">{item.subject}</span>
                      <span className="text-sm text-green-600 font-bold">
                        {item.score}%
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {item.recommendation}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Weaknesses */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-orange-500" />
                Weaknesses
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {weaknesses.map((item, i) => (
                  <div key={i} className="border rounded-lg p-3">
                    <div className="flex justify-between items-center mb-1">
                      <span className="font-medium">{item.subject}</span>
                      <span className="text-sm text-orange-600 font-bold">
                        {item.score}%
                      </span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {item.recommendation}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Recommendations */}
          <Card>
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <Lightbulb className="h-5 w-5 text-yellow-500" />
                Recommendations
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {recommendations.map((rec, i) => (
                  <div key={i} className="border rounded-lg p-3">
                    <div className="flex items-center gap-2 mb-1">
                      <span
                        className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                          rec.priority === "high"
                            ? "bg-red-100 text-red-800"
                            : rec.priority === "medium"
                            ? "bg-yellow-100 text-yellow-800"
                            : "bg-green-100 text-green-800"
                        }`}
                      >
                        {(rec.priority ?? "medium").toUpperCase()}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        {rec.type}
                      </span>
                    </div>
                    <p className="text-sm">{rec.action}</p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          {/* Risk Indicators */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="text-lg flex items-center gap-2">
                <ShieldAlert className="h-5 w-5 text-red-500" />
                Risk Indicators
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {riskIndicators.map((risk, i) => (
                  <div
                    key={i}
                    className={`border rounded-lg p-4 ${
                      risk.severity === "high"
                        ? "border-red-200 bg-red-50"
                        : risk.severity === "medium"
                        ? "border-yellow-200 bg-yellow-50"
                        : "border-green-200 bg-green-50"
                    }`}
                  >
                    <div className="flex items-center gap-2 mb-1">
                      <AlertTriangle className="h-5 w-5" />
                      <span className="font-medium">{risk.type}</span>
                    </div>
                    <p className="text-sm text-muted-foreground">
                      {risk.message}
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
