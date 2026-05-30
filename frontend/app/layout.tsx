import type { Metadata } from "next";
import "./globals.css";
import { Providers } from "./providers";
import { Sidebar } from "@/components/sidebar";
import { ErrorBoundary } from "@/components/error-boundary";

export const metadata: Metadata = {
  title: "Gurukula AI",
  description: "Intelligent learning platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body>
        <Providers>
          <div className="flex min-h-screen">
            <Sidebar />
            <main className="flex-1">
              <ErrorBoundary>{children}</ErrorBoundary>
            </main>
          </div>
        </Providers>
      </body>
    </html>
  );
}
