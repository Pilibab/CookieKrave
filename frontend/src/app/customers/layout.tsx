import Sidebar from "@/components/layout/Sidebar";
import AdminGuard from "@/components/layout/AdminGuard";

export default function PanelLayout({ children }: { children: React.ReactNode }) {
  return (
    <AdminGuard>
      <div style={{ minHeight: "100vh", background: "var(--cream)" }}>
        <Sidebar />
        <div style={{
          paddingTop: "var(--navbar-h)",
          padding: "calc(var(--navbar-h) + 28px) 40px 40px",
          maxWidth: 1200,
          margin: "0 auto",
        }}>
          {children}
        </div>
      </div>
    </AdminGuard>
  );
}
