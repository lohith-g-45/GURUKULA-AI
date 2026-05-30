"use client";

import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { api } from "@/services/api";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ErrorState } from "@/components/common/error-state";
import { PageHeader } from "@/components/common/PageHeader";
import { ProgressBar } from "@/components/common/ProgressBar";
import { useUserProfile } from "@/contexts/user-profile-context";
import {
  Calendar,
  BookOpen,
  Clock,
  Target,
  CheckCircle,
  AlertCircle,
  BarChart3,
  TrendingUp,
  Award,
  RefreshCw,
} from "lucide-react";
import type { PlanningData, DashboardData } from "@/types/dashboard";

export default function RoadmapPage() {
  const router = useRouter();
  const { profile, isLoading: profileLoading } = useUserProfile();
  const [activeTab, setActiveTab] = useState<"roadmap" | "schedule" | "milestones">("roadmap");

  const { data: dashboardData, isLoading: dashboardLoading, error: dashboardError, refetch: refetchDashboard } = 
    useQuery<DashboardData, Error>({
      queryKey: ["dashboard-stats"],
      queryFn: async () => {
        const res = await api.dashboard.get();
        return res.data;
      },
      staleTime: 60000, // 1 minute
      refetchOnWindowFocus: false,
    });

  const { data: planningData, isLoading: planningLoading, error: planningError, refetch: refetchPlanning } = 
    useQuery({
      queryKey: ["planner"],
      queryFn: async () => {
        const res = await api.agent.getPlanner({
          exam: profile?.exam || "KAS",
          readiness_score: profile?.readiness_score || 70,
          available_hours_per_day: profile?.available_hours_per_day || 6,
          weak_subjects: profile?.weak_subjects || [],
        });
        return res.data.data;
      },
      enabled: !!profile,
      staleTime: 60000, // 1 minute
      refetchOnWindowFocus: false,
    });

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

  const isLoading = dashboardLoading || planningLoading;
  const error = dashboardError || planningError;
  const refetch = () => {
    refetchDashboard();
    refetchPlanning();
  };

  if (isLoading) {
    return (
      <div className="p-8">
        <PageHeader title="Preparation Roadmap" description="Your personalized study plan" />
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
          {[1, 2, 3, 4].map((i) => (
            <Skeleton key={i} className="h-40" />
          ))}
        </div>
        <Skeleton className="h-96" />
      </div>
    );
  }

  if (error) {
    const errorMessage =
      error instanceof Error ? error.message : "Failed to load data";
    return (
      <div className="p-8">
        <ErrorState
          message={errorMessage}
          onRetry={refetch}
        />
      </div>
    );
  }

  // Safely access data with fallbacks
  const plan = (planningData as PlanningData) || {
    preparation_roadmap: { duration_months: 0, stages: [] },
    subject_plan: [],
    weekly_schedule: { daily_targets: [], mock_test_frequency: "Weekly", study_days_per_week: 6, daily_hours: 6 },
    daily_schedule: [],
    milestones: [],
    revision_cycles: [],
    mock_schedule: null
  };
  
  const stats = dashboardData?.data;

  return (
    <div className="p-8">
      <PageHeader title="Preparation Roadmap" description="Your personalized study plan" />

      {/* Dashboard Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
        <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-blue-600 flex items-center gap-2">
              <Target className="h-4 w-4" />
              Readiness Score
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-700">{stats?.readiness_score || 0}%</div>
            <ProgressBar value={stats?.readiness_score || 0} max={100} className="mt-2" />
          </CardContent>
        </Card>
        <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-green-600 flex items-center gap-2">
              <CheckCircle className="h-4 w-4" />
              Total Tasks
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-700">{stats?.total_tasks || 0}</div>
            <p className="text-sm text-green-600 mt-1">{stats?.completed_tasks || 0} completed</p>
          </CardContent>
        </Card>
        <Card className="bg-gradient-to-br from-yellow-50 to-yellow-100 border-yellow-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-yellow-600 flex items-center gap-2">
              <Clock className="h-4 w-4" />
              Study Hours Today
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-yellow-700">{stats?.study_hours_today || 0}h</div>
            <p className="text-sm text-yellow-600 mt-1">{plan?.weekly_schedule?.daily_hours || 6}h planned</p>
          </CardContent>
        </Card>
        <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm text-purple-600 flex items-center gap-2">
              <Calendar className="h-4 w-4" />
              Duration
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-purple-700">{plan?.preparation_roadmap?.duration_months || 0} months</div>
            <p className="text-sm text-purple-600 mt-1">{plan?.preparation_roadmap?.stages?.length || 0} stages</p>
          </CardContent>
        </Card>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-4 mb-6 border-b border-gray-200">
        <button
          onClick={() => setActiveTab("roadmap")}
          className={`pb-3 px-4 font-medium border-b-2 transition-colors ${
            activeTab === "roadmap"
              ? "border-blue-500 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <div className="flex items-center gap-2">
            <TrendingUp className="h-4 w-4" />
            Preparation Roadmap
          </div>
        </button>
        <button
          onClick={() => setActiveTab("schedule")}
          className={`pb-3 px-4 font-medium border-b-2 transition-colors ${
            activeTab === "schedule"
              ? "border-blue-500 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <div className="flex items-center gap-2">
            <Clock className="h-4 w-4" />
            Weekly & Daily Schedule
          </div>
        </button>
        <button
          onClick={() => setActiveTab("milestones")}
          className={`pb-3 px-4 font-medium border-b-2 transition-colors ${
            activeTab === "milestones"
              ? "border-blue-500 text-blue-600"
              : "border-transparent text-gray-500 hover:text-gray-700"
          }`}
        >
          <div className="flex items-center gap-2">
            <Award className="h-4 w-4" />
            Milestones
          </div>
        </button>
        <button
          onClick={refetch}
          className="ml-auto pb-3 px-4 text-gray-500 hover:text-blue-600 transition-colors"
        >
          <RefreshCw className="h-4 w-4" />
        </button>
      </div>

      {/* Roadmap Tab */}
      {activeTab === "roadmap" && (
        <div className="space-y-6">
          {/* Study Stages */}
          {plan?.preparation_roadmap?.stages && plan.preparation_roadmap.stages.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BarChart3 className="h-5 w-5 text-blue-500" />
                  Study Stages
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {plan.preparation_roadmap.stages.map((stage, idx) => (
                    <Card key={idx} className="border-l-4 border-l-blue-500">
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">{stage.stage_name}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-gray-600 mb-2">
                          <Calendar className="h-3 w-3 inline mr-1" />
                          {stage.duration_weeks} weeks
                        </p>
                        <p className="text-sm text-gray-600 mb-2">
                          <Clock className="h-3 w-3 inline mr-1" />
                          {stage.weekly_hours}h/week
                        </p>
                        <div className="flex flex-wrap gap-1">
                          {stage.focus_subjects?.map((subj, i) => (
                            <span key={i} className="text-xs bg-blue-100 text-blue-700 px-2 py-0.5 rounded">
                              {subj}
                            </span>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Subject Plan */}
          {plan?.subject_plan && plan.subject_plan.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <BookOpen className="h-5 w-5 text-green-500" />
                  Subject Plan
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {plan.subject_plan.map((subj, idx) => (
                    <Card key={idx}>
                      <CardHeader className="pb-2">
                        <div className="flex justify-between items-center">
                          <CardTitle className="text-base">{subj.subject}</CardTitle>
                          <span className={`text-xs font-bold px-2 py-0.5 rounded ${
                            subj.priority === "High" ? "bg-red-100 text-red-700" : "bg-yellow-100 text-yellow-700"
                          }`}>
                            {subj.priority}
                          </span>
                        </div>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-gray-600 mb-2">
                          {subj.allocated_hours} hours allocated
                        </p>
                        <div className="text-xs text-gray-500">
                          Topics: {subj.topics?.map(t => t.name).join(", ") || ""}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Revision Cycles */}
          {plan.revision_cycles && plan.revision_cycles.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <RefreshCw className="h-5 w-5 text-purple-500" />
                  Revision Cycles
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {plan.revision_cycles.map((rev, idx) => (
                    <Card key={idx}>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">{rev.subject}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <p className="text-sm text-gray-600 mb-1">
                          Frequency: {rev.revision_frequency}
                        </p>
                        <p className="text-xs text-gray-500">
                          Spaced repetition: Days {rev.revision_days?.join(", ") || ""}
                        </p>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Mock Schedule */}
          {plan.mock_schedule && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <AlertCircle className="h-5 w-5 text-orange-500" />
                  Mock Schedule
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <p className="font-medium text-gray-800">Mock Type</p>
                    <p className="text-gray-600">{plan.mock_schedule.mock_type}</p>
                  </div>
                  <div>
                    <p className="font-medium text-gray-800">Frequency</p>
                    <p className="text-gray-600">{plan.mock_schedule.frequency}</p>
                  </div>
                  <div className="md:col-span-2">
                    <p className="font-medium text-gray-800">Focus Subjects</p>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {plan.mock_schedule.focus_subjects?.map((subj, i) => (
                        <span key={i} className="text-xs bg-orange-100 text-orange-700 px-2 py-0.5 rounded">
                          {subj}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Schedule Tab */}
      {activeTab === "schedule" && (
        <div className="space-y-6">
          {/* Weekly Targets */}
          {plan?.weekly_schedule?.daily_targets && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Target className="h-5 w-5 text-blue-500" />
                  Weekly Targets
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">Daily Targets</h4>
                    <ul className="space-y-2">
                      {plan.weekly_schedule.daily_targets.map((target, i) => (
                        <li key={i} className="flex items-start gap-2">
                          <CheckCircle className="h-4 w-4 text-green-500 mt-0.5 flex-shrink-0" />
                          <span>{target}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                  <div>
                    <h4 className="font-medium text-gray-800 mb-2">Schedule Details</h4>
                    <p className="text-gray-600">Study days per week: {plan.weekly_schedule.study_days_per_week || 6}</p>
                    <p className="text-gray-600">Daily study hours: {plan.weekly_schedule.daily_hours || 6}h</p>
                    <p className="text-gray-600">Mock tests: {plan.weekly_schedule.mock_test_frequency || "Weekly"}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {/* Daily Schedule */}
          {plan.daily_schedule && plan.daily_schedule.length > 0 && (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Clock className="h-5 w-5 text-green-500" />
                  Daily Schedule
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {plan.daily_schedule.map((day, idx) => (
                    <Card key={idx}>
                      <CardHeader className="pb-2">
                        <CardTitle className="text-base">{day.day}</CardTitle>
                      </CardHeader>
                      <CardContent>
                        <div className="space-y-2">
                          {day.items?.map((item, i) => (
                            <div key={i} className="border-l-2 border-blue-500 pl-3">
                              <p className="text-xs text-gray-500">{item.time_slot}</p>
                              <p className="font-medium text-sm">{item.subject}</p>
                              <p className="text-xs text-gray-600">{item.activity}</p>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Milestones Tab */}
      {activeTab === "milestones" && (
        <div className="space-y-6">
          {plan.milestones && plan.milestones.length > 0 ? (
            <Card>
              <CardHeader>
                <CardTitle className="text-lg flex items-center gap-2">
                  <Award className="h-5 w-5 text-yellow-500" />
                  Key Milestones
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {plan.milestones.map((milestone, idx) => (
                    <Card key={idx} className="border-l-4 border-l-yellow-500">
                      <CardHeader className="pb-2">
                        <div className="flex justify-between items-start">
                          <CardTitle className="text-base">{milestone.description}</CardTitle>
                          {milestone.target_stage && (
                            <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                              {milestone.target_stage}
                            </span>
                          )}
                        </div>
                      </CardHeader>
                      <CardContent>
                        <div className="mb-2">
                          <p className="text-sm text-gray-600 font-medium">Criteria:</p>
                          <ul className="list-disc ml-4 text-sm text-gray-500">
                            {milestone.criteria?.map((c, i) => (
                              <li key={i}>{c}</li>
                            ))}
                          </ul>
                        </div>
                        {milestone.reward && (
                          <p className="text-sm text-yellow-600 font-medium">
                            Reward: {milestone.reward}
                          </p>
                        )}
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          ) : (
            <Card>
              <CardContent className="text-center py-8">
                <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-2" />
                <p className="text-gray-500">No milestones available</p>
              </CardContent>
            </Card>
          )}
        </div>
      )}
    </div>
  );
}
