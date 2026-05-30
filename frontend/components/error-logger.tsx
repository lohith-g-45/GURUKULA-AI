"use client";

import { useEffect } from "react";

export function ErrorLogger() {
  useEffect(() => {
    const handleError = (event: ErrorEvent) => {
      console.error("Global error caught:", event);
      console.error("Error message:", event.message);
      console.error("Error filename:", event.filename);
      console.error("Error lineno:", event.lineno);
      console.error("Error colno:", event.colno);
      console.error("Error object:", event.error);
    };

    const handleRejection = (event: PromiseRejectionEvent) => {
      console.error("Unhandled promise rejection:", event);
      console.error("Rejection reason:", event.reason);
    };

    window.addEventListener("error", handleError);
    window.addEventListener("unhandledrejection", handleRejection);

    return () => {
      window.removeEventListener("error", handleError);
      window.removeEventListener("unhandledrejection", handleRejection);
    };
  }, []);

  return null;
}
