"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";

export default function Step3Page() {
  const router = useRouter();
  const { profile, updateProfile } = useUserProfile();
  const [readiness, setReadiness] = useState(profile?.readiness_score || 50);
  const [hours, setHours] = useState(profile?.available_hours_per_day || 6);

  const handleNext = () => {
    updateProfile({ readiness_score: readiness, available_hours_per_day: hours });
    router.push("/onboarding/step-4");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.push("/onboarding/step-2")}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Your readiness</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Readiness Score: {readiness}%
              </label>
              <input
                type="range"
                min="0"
                max="100"
                value={readiness}
                onChange={(e) => setReadiness(Number(e.target.value))}
                className="w-full"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Available Study Hours per Day: {hours}h
              </label>
              <input
                type="range"
                min="1"
                max="24"
                step="0.5"
                value={hours}
                onChange={(e) => setHours(Number(e.target.value))}
                className="w-full"
              />
            </div>
            <Button className="w-full" onClick={handleNext}>
              Next
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
