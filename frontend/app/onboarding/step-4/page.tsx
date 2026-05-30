"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, ArrowRight } from "lucide-react";
import { useUserProfile } from "@/contexts/user-profile-context";

const SUBJECTS = [
  "History",
  "Geography",
  "Polity",
  "Economy",
  "Environment",
  "Science & Technology",
  "Current Affairs",
  "Mathematics",
  "English",
  "Reasoning",
];

export default function Step4Page() {
  const router = useRouter();
  const { profile, updateProfile } = useUserProfile();
  const [selectedSubjects, setSelectedSubjects] = useState<string[]>(
    profile?.weak_subjects || []
  );

  const toggleSubject = (subject: string) => {
    setSelectedSubjects((prev) =>
      prev.includes(subject)
        ? prev.filter((s) => s !== subject)
        : [...prev, subject]
    );
  };

  const handleNext = () => {
    updateProfile({ weak_subjects: selectedSubjects });
    router.push("/onboarding/step-5");
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8">
        <Button
          variant="ghost"
          className="mb-6"
          onClick={() => router.push("/onboarding/step-3")}
        >
          <ArrowLeft className="w-4 h-4 mr-2" />
          Back
        </Button>
        <Card>
          <CardHeader>
            <CardTitle className="text-2xl">Select weak subjects</CardTitle>
          </CardHeader>
          <CardContent className="space-y-3">
            {SUBJECTS.map((subject) => (
              <Button
                key={subject}
                variant={selectedSubjects.includes(subject) ? "default" : "secondary"}
                className="w-full justify-start text-left"
                onClick={() => toggleSubject(subject)}
              >
                {subject}
              </Button>
            ))}
            <Button className="w-full mt-6" onClick={handleNext}>
              Next
              <ArrowRight className="ml-2 w-4 h-4" />
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
