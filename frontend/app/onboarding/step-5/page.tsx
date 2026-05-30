"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";

const GOALS = [
  "Clear Prelims",
  "Clear Mains",
  "Get Top 100 Rank",
  "Complete Syllabus in 3 Months",
  "Complete Syllabus in 6 Months",
  "Daily Revision",
  "Weekly Mock Tests",
];

export default function Step5Page() {
  const router = useRouter();
  const { profile, updateProfile } = useUserProfile();
  const [selectedGoals, setSelectedGoals] = useState<string[]>(
    profile?.study_goals || []
  );

  const toggleGoal = (goal: string) => {
    setSelectedGoals((prev) =>
      prev.includes(goal) ? prev.filter((g) => g !== goal) : [...prev, goal]
    );
  };

  const handleNext = () => {
    updateProfile({ study_goals: selectedGoals });
    router.push("/onboarding/review");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.push("/onboarding/step-4")}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Select your goals</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {GOALS.map((goal) => (
              <Button
                key={goal}
                variant={selectedGoals.includes(goal) ? "default" : "secondary"}
                className="w-full justify-start text-left"
                onClick={() => toggleGoal(goal)}
              >
                {goal}
              </Button>
            ))}
            <Button className="w-full mt-6" onClick={handleNext}>
              Review
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
