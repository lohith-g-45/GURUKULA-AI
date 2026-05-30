"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Spinner } from "@/components/ui/spinner";
import { ArrowLeft, CheckCircle } from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";
import { api } from "@/services/api";

export default function ReviewPage() {
  const router = useRouter();
  const { profile, setProfile } = useUserProfile();
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!profile) return;
    setIsSubmitting(true);
    setError(null);
    try {
      const response = await api.user.updateProfile(profile);
      if (response.data.success) {
        setProfile(response.data.data);
        router.push("/onboarding/success");
      } else {
        setError(response.data.message || "Failed to submit profile");
      }
    } catch (err) {
      setError("An error occurred while submitting. Please try again.");
      console.error("Failed to submit profile:", err);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!profile) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.push("/onboarding/step-5")}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Review your profile</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-gray-500">Name</p>
              <p className="font-medium">{profile.name || "Not provided"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="font-medium">{profile.email || "Not provided"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Exam</p>
              <p className="font-medium">{profile.exam}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Readiness Score</p>
              <p className="font-medium">{profile.readiness_score}%</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Study Hours/Day</p>
              <p className="font-medium">{profile.available_hours_per_day}h</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Weak Subjects</p>
              <p className="font-medium">
                {profile.weak_subjects?.length ? profile.weak_subjects.join(", ") : "None selected"}
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Study Goals</p>
              <p className="font-medium">
                {profile.study_goals?.length ? profile.study_goals.join(", ") : "None selected"}
              </p>
            </div>
            {error && (
              <div className="p-4 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
                {error}
              </div>
            )}
            <Button
              className="w-full mt-6"
              onClick={handleSubmit}
              disabled={isSubmitting}
            >
              {isSubmitting ? (
                <>
                  <Spinner className="w-4 h-4 mr-2" />
                  Submitting...
                </>
              ) : (
                <>
                  Confirm & Submit
                  <CheckCircle className="ml-2 w-4 h-4" />
                </>
              )}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
