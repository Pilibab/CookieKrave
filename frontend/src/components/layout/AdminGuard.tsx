"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";
import { IS_MOCK } from "@/lib/api";

export default function AdminGuard({ children }: { children: React.ReactNode }) {
  const { user, loading, isAdmin } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // In mock mode, auth is bypassed — admin is simulated
    if (IS_MOCK) return;
    if (!loading && user && !isAdmin) {
      router.replace("/auth/login?error=unauthorized");
    }
  }, [loading, user, isAdmin, router]);

  // Mock mode: skip all auth checks, render immediately
  if (IS_MOCK) return <>{children}</>;

  if (loading) {
    return (
      <div style={{
        display: "flex", alignItems: "center", justifyContent: "center",
        height: "100vh", background: "#f2f3f8",
      }}>
        <div style={{
          width: 28, height: 28,
          border: "3px solid #e2e4ef",
          borderTopColor: "#0d1240",
          borderRadius: "50%",
          animation: "spin 0.7s linear infinite",
        }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (!isAdmin) return null;

  return <>{children}</>;
}
