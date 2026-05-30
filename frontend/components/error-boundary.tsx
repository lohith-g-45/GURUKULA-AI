"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { ErrorState } from "@/components/common/error-state";

interface Props {
  children: ReactNode;
}

interface State {
  hasError: boolean;
  errorMessage?: string;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: unknown): State {
    let errorMessage = "Something went wrong";
    if (error instanceof Error) {
      errorMessage = error.message;
    } else if (typeof error === "string") {
      errorMessage = error;
    } else if (error && typeof error === "object" && "message" in error) {
      errorMessage = String(error.message);
    }
    return { hasError: true, errorMessage };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Error caught by boundary:", error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <ErrorState
          message={this.state.errorMessage || "Something went wrong"}
          onRetry={() => this.setState({ hasError: false, errorMessage: undefined })}
        />
      );
    }

    return this.props.children;
  }
}
