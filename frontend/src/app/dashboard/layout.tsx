import Sidebar from "@/components/layout/Sidebar";
import AdminGuard from "@/components/layout/AdminGuard";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <AdminGuard>
      <div style={{ minHeight: "100vh", background: "var(--cream)" }}>
        <Sidebar />
        <div style={{ paddingTop: "var(--navbar-h)" }}>
          {children}
        </div>
      </div>
    </AdminGuard>
  );
}
