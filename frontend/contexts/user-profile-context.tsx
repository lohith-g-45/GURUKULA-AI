"use client";

import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import type { UserProfile } from "@/types/dashboard";

interface UserProfileContextType {
  profile: UserProfile | null;
  isLoading: boolean;
  setProfile: (profile: UserProfile | null) => void;
  updateProfile: (updates: Partial<UserProfile>) => void;
  clearProfile: () => void;
}

const UserProfileContext = createContext<UserProfileContextType | undefined>(undefined);

const STORAGE_KEY = "gurukula_user_profile";

export function UserProfileProvider({ children }: { children: ReactNode }) {
  const [profile, setProfileState] = useState<UserProfile | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) {
      try {
        setProfileState(JSON.parse(saved));
      } catch (e) {
        console.error("Failed to parse stored profile:", e);
      }
    }
    setIsLoading(false);
  }, []);

  const setProfile = (newProfile: UserProfile | null) => {
    setProfileState(newProfile);
    if (newProfile) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(newProfile));
    } else {
      localStorage.removeItem(STORAGE_KEY);
    }
  };

  const updateProfile = (updates: Partial<UserProfile>) => {
    setProfileState((prev) => {
      const updated = { ...(prev || {}), ...updates };
      localStorage.setItem(STORAGE_KEY, JSON.stringify(updated));
      return updated;
    });
  };

  const clearProfile = () => {
    setProfileState(null);
    localStorage.removeItem(STORAGE_KEY);
  };

  return (
    <UserProfileContext.Provider value={{ profile, isLoading, setProfile, updateProfile, clearProfile }}>
      {children}
    </UserProfileContext.Provider>
  );
}

export function useUserProfile() {
  const context = useContext(UserProfileContext);
  if (!context) {
    throw new Error("useUserProfile must be used within a UserProfileProvider");
  }
  return context;
}
