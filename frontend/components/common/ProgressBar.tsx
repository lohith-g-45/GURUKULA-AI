import React from "react";
import { cn } from "@/components/ui/lib/utils";

interface ProgressBarProps {
  value: number;
  max?: number;
  className?: string;
  color?: string;
}

export function ProgressBar({ value, max = 100, className, color }: ProgressBarProps) {
  const percentage = Math.min(100, Math.max(0, (value / max) * 100));
  
  return (
    <div className={cn("w-full", className)}>
      <div className="flex justify-between mb-2">
        <span className="text-sm font-semibold text-muted-foreground">
          {Math.round(value)}%
        </span>
      </div>
      <div className="w-full bg-muted rounded-full h-3 overflow-hidden">
        <div
          className="h-full rounded-full transition-all duration-1000 ease-out"
          style={{
            width: `${percentage}%`,
            background: color || (percentage >= 70 
              ? "linear-gradient(to right, #14b8a6, #0d9488)" 
              : percentage >= 40 
              ? "linear-gradient(to right, #f97316, #ea580c)" 
              : "linear-gradient(to right, #f8e8c4, #d97706)"),
          }}
        />
      </div>
    </div>
  );
}
