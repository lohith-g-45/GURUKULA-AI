"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, BookOpen, Calendar, Settings, Sun, Moon, Menu, X, Target, TrendingUp, Lightbulb, Clock, Star, BarChart3, Activity } from "lucide-react";
import { useTheme } from "@/contexts/theme-context";
import { useHealth } from "@/hooks/use-health";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Spinner } from "@/components/ui/spinner";

export function Sidebar() {
  const { theme, toggleTheme } = useTheme();
  const { data: healthData, isLoading: healthLoading, error: healthError } = useHealth();
  const pathname = usePathname();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const navItems = [
    { href: "/", label: "Dashboard", icon: Home },
    { href: "/tasks", label: "Tasks", icon: Star },
    { href: "/insights", label: "Insights", icon: BarChart3 },
    { href: "/monitoring", label: "Monitoring", icon: Activity },
    { href: "/revision", label: "Revision", icon: Clock },
    { href: "/replan", label: "Replan", icon: TrendingUp },
    { href: "/roadmap", label: "Roadmap", icon: Target },
    { href: "/study", label: "Study", icon: BookOpen },
    { href: "/calendar", label: "Calendar", icon: Calendar },
    { href: "/settings", label: "Settings", icon: Settings },
    { href: "/debug", label: "Debug", icon: Lightbulb },
  ];

  const isHealthy = healthData?.status === "healthy";

  const SidebarContent = () => (
    <div className="w-64 border-r bg-card p-6 flex flex-col h-full transition-all duration-300">
      <div className="mb-8">
        <h2 className="text-2xl font-bold bg-gradient-to-r from-orange-500 to-teal-500 bg-clip-text text-transparent">Gurukula AI</h2>
      </div>

      <nav className="space-y-2 flex-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setIsMobileMenuOpen(false)}
              className={`flex items-center gap-3 px-4 py-3 rounded-2xl text-sm font-semibold transition-all duration-300 group ${
                isActive
                  ? "bg-gradient-to-r from-orange-500 to-teal-500 text-white shadow-lg hover:shadow-xl hover:scale-[1.02]"
                  : "text-muted-foreground hover:bg-accent hover:text-foreground hover:scale-[1.01]"
              }`}
            >
              <item.icon className={`h-5 w-5 transition-all duration-300 ${isActive ? "" : "group-hover:scale-110"}`} />
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      <div className="space-y-4 pt-4 border-t border-border">
        <div className="flex items-center justify-between">
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            className="rounded-full hover:bg-accent hover:scale-110 transition-all duration-300"
          >
            {theme === "light" ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
          </Button>

          <div className="flex items-center gap-2">
            {healthLoading ? (
              <Spinner className="h-4 w-4" />
            ) : healthError ? (
              <div className="w-3 h-3 rounded-full bg-red-500 animate-pulse" />
            ) : isHealthy ? (
              <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
            ) : (
              <div className="w-3 h-3 rounded-full bg-orange-500 animate-pulse" />
            )}
            <span className="text-xs text-muted-foreground">
              {healthLoading ? "Checking..." : healthError ? "Offline" : isHealthy ? "Online" : "Unknown"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Mobile menu button */}
      <Button
        variant="ghost"
        size="icon"
        className="fixed top-4 left-4 z-50 md:hidden rounded-2xl shadow-lg hover:shadow-xl transition-all duration-300"
        onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
      >
        {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
      </Button>

      {/* Desktop sidebar */}
      <div className="hidden md:block">
        <SidebarContent />
      </div>

      {/* Mobile sidebar */}
      {isMobileMenuOpen && (
        <div className="fixed inset-0 z-40 md:hidden">
          <div className="fixed inset-0 bg-black/50 backdrop-blur-sm" onClick={() => setIsMobileMenuOpen(false)} />
          <div className="fixed left-0 top-0 h-full">
            <SidebarContent />
          </div>
        </div>
      )}
    </>
  );
}
