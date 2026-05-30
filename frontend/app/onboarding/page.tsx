"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Brain, ArrowRight } from "lucide-react";

export default function WelcomePage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8 text-center">
        <div className="w-24 h-24 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-6">
          <Brain className="w-12 h-12 text-white" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Welcome to Gurukula AI!</h1>
        <p className="text-gray-600 mb-8">
          Let&apos;s personalize your learning journey. Answer a few questions to help us create the perfect study plan for you.
        </p>
        <Button
          className="w-full py-6 text-lg"
          onClick={() => router.push("/onboarding/step-1")}
        >
          Get Started
          <ArrowRight className="ml-2 w-5 h-5" />
        </Button>
      </div>
    </div>
  );
}
