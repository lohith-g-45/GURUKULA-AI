"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";

const EXAMS = ["KAS", "UPSC", "SSC", "Bank PO", "GATE", "NEET", "JEE"];

export default function Step2Page() {
  const router = useRouter();
  const { profile, updateProfile } = useUserProfile();
  const [selectedExam, setSelectedExam] = useState(profile?.exam || "");

  const handleNext = () => {
    if (selectedExam) {
      updateProfile({ exam: selectedExam });
      router.push("/onboarding/step-3");
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.push("/onboarding/step-1")}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Select your exam</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {EXAMS.map((exam) => (
              <Button
                key={exam}
                variant={selectedExam === exam ? "default" : "secondary"}
                className="w-full justify-start text-left"
                onClick={() => setSelectedExam(exam)}
              >
                {exam}
              </Button>
            ))}
            <Button
              className="w-full mt-6"
              onClick={handleNext}
              disabled={!selectedExam}
            >
              Next
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
