"use client";

import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { CheckCircle, Home } from "lucide-react";

export default function SuccessPage() {
  const router = useRouter();

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-500 via-purple-500 to-pink-500 flex items-center justify-center p-6">
      <div className="max-w-md w-full bg-white rounded-3xl shadow-2xl p-8 text-center">
        <div className="w-24 h-24 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <CheckCircle className="w-12 h-12 text-green-600" />
        </div>
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Profile Created!</h1>
        <p className="text-gray-600 mb-8">
          Your learning profile has been successfully created. Let&apos;s start your journey!
        </p>
        <Button
          className="w-full py-6 text-lg"
          onClick={() => router.push("/")}
        >
          Go to Dashboard
          <Home className="ml-2 w-5 h-5" />
        </Button>
      </div>
    </div>
  );
}
