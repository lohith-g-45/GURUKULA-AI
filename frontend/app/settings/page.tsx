"use client";

import { useState } from "react";
import { PageHeader } from "@/components/common/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { api } from "@/services/api";
import { useToast } from "@/contexts/ToastContext";
import type { UserProfile } from "@/types/dashboard";

export default function SettingsPage() {
  const [formData, setFormData] = useState<UserProfile>({
    name: "",
    email: "",
    exam: "KAS",
    readiness_score: 70,
    available_hours_per_day: 6,
    weak_subjects: [],
    study_goals: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const { addToast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      await api.user.updateProfile(formData);
      addToast("Profile updated successfully!", "success");
    } catch (error) {
      console.error("Error updating profile:", error);
      addToast("Failed to update profile", "error");
    } finally {
      setIsLoading(false);
    }
  };

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]:
        name === "readiness_score" || name === "available_hours_per_day"
          ? parseFloat(value) || 0
          : value,
    }));
  };

  const handleWeakSubjectsChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setFormData((prev) => ({
      ...prev,
      weak_subjects: value.split(",").map((s) => s.trim()).filter(Boolean),
    }));
  };

  const handleStudyGoalsChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setFormData((prev) => ({
      ...prev,
      study_goals: value.split("\n").map((s) => s.trim()).filter(Boolean),
    }));
  };

  return (
    <div className="p-8">
      <PageHeader
        title="Settings"
        description="Manage your profile and preferences"
      />

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">User Profile</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Name</label>
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border rounded-md bg-background"
                  placeholder="Your name"
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Email</label>
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border rounded-md bg-background"
                  placeholder="your@email.com"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium mb-1">Exam</label>
                <select
                  name="exam"
                  value={formData.exam}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border rounded-md bg-background"
                >
                  <option value="KAS">KAS</option>
                  <option value="UPSC">UPSC</option>
                  <option value="SSC">SSC</option>
                  <option value="Other">Other</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">
                  Readiness Score (%)
                </label>
                <input
                  type="number"
                  name="readiness_score"
                  min="0"
                  max="100"
                  value={formData.readiness_score}
                  onChange={handleChange}
                  className="w-full px-3 py-2 border rounded-md bg-background"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Available Hours Per Day
              </label>
              <input
                type="number"
                name="available_hours_per_day"
                min="0"
                max="24"
                step="0.5"
                value={formData.available_hours_per_day}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-md bg-background"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Weak Subjects (comma-separated)
              </label>
              <input
                type="text"
                value={formData.weak_subjects?.join(", ") || ""}
                onChange={handleWeakSubjectsChange}
                className="w-full px-3 py-2 border rounded-md bg-background"
                placeholder="Polity, History, Geography"
              />
            </div>

            <div>
              <label className="block text-sm font-medium mb-1">
                Study Goals (one per line)
              </label>
              <textarea
                value={formData.study_goals?.join("\n") || ""}
                onChange={handleStudyGoalsChange}
                rows={4}
                className="w-full px-3 py-2 border rounded-md bg-background"
                placeholder="Complete Polity by end of month&#10;Take 3 mock tests&#10;Revise Modern History"
              />
            </div>

            <Button type="submit" disabled={isLoading}>
              {isLoading ? "Saving..." : "Save Changes"}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
