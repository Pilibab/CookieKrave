"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/useAuth";

const NAV = [
  { href: "/dashboard", label: "Home" },
  { href: "/orders",    label: "Orders" },
  { href: "/products",  label: "Products" },
  { href: "/inventory", label: "Inventory" },
  { href: "/customers", label: "Customers" },
  { href: "/reports",   label: "Reports" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  return (
    <div className="navbar-wrapper">
    <nav className="navbar">
      {/* Brand */}
      <Link href="/dashboard" className="navbar-brand">
        <img src="/CKWebLogo.png" alt="Cookie Krave" className="navbar-logo" />
      </Link>

      {/* Nav links */}
      <div className="navbar-nav">
        {NAV.map(({ href, label }) => {
          const active = pathname === href || pathname.startsWith(href + "/");
          return (
            <Link
              key={href}
              href={href}
              className={`navbar-link${active ? " active" : ""}`}
            >
              {label}
            </Link>
          );
        })}
      </div>

      {/* User area */}
      <div className="navbar-user">
        <span style={{ color: '#9ca3af' }}>Admin</span>
        <div className="navbar-avatar" style={{ cursor: "pointer" }} onClick={logout}>
          {user?.image
            ? <img src={user.image} alt={user.name} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            : (
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                <circle cx="12" cy="7" r="4"/>
              </svg>
            )
          }
        </div>
      </div>

      {/* Full-width thin gray line with space above it */}
      <div className="navbar-underline" />
    </nav>
    </div>
  );
}
