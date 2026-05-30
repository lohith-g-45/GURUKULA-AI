import React from "react";
import { Card, CardContent, CardHeader } from "@/components/ui/card";

interface StatCardProps {
  title: string;
  value: string | number;
  icon?: React.ReactNode;
  description?: string;
  trend?: "up" | "down" | "neutral";
}

export function StatCard({ title, value, icon, description, trend }: StatCardProps) {
  return (
    <Card className="relative overflow-hidden">
      {/* Gradient top border */}
      <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-orange-500 to-teal-500"></div>
      <CardHeader className="flex flex-row items-center justify-between pb-2 pt-6">
        <div className="space-y-1">
          <p className="text-sm font-semibold text-muted-foreground">{title}</p>
          <h3 className="text-3xl font-bold">{value}</h3>
        </div>
        {icon && (
          <div className="p-3 rounded-2xl bg-gradient-to-r from-orange-500/10 to-teal-500/10 text-primary transition-all duration-300 hover:scale-110">
            {icon}
          </div>
        )}
      </CardHeader>
      {description && (
        <CardContent>
          <div className="flex items-center text-sm">
            {trend === "up" && <span className="text-green-500 mr-1">↑</span>}
            {trend === "down" && <span className="text-red-500 mr-1">↓</span>}
            <span className="text-muted-foreground">{description}</span>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
