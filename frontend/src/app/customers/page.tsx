"use client";

import { useState } from "react";
import { useFetch } from "@/hooks/useFetch";
import { customersApi } from "@/lib/api";
import type { Customer } from "@/types";

export default function CustomersPage() {
  const [page, setPage] = useState(1);
  const { data, loading, refetch } = useFetch(() => customersApi.list(page, 20), [page]);
  const [showForm, setShowForm] = useState(false);
  const [search, setSearch] = useState("");

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title" style={{ color: "var(--navy)" }}>Customers</h1>
          <p style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 2 }}>
            {data?.total ?? 0} customers
          </p>
        </div>
        <div style={{ display: "flex", gap: 10, alignItems: "center" }}>
          <div className="search-bar">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
            </svg>
            <input
              placeholder="Search customers..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
          </div>
          <button className="btn btn-primary" onClick={() => setShowForm(true)}>+ Add Customer</button>
        </div>
      </div>

      {showForm && (
        <CustomerForm onClose={() => setShowForm(false)} onSaved={refetch} />
      )}

      <div className="card">
        {loading && <div className="spinner" />}
        {!loading && (
          <>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    <th>Order ID</th>
                    <th>Customer</th>
                    <th>Date & Time</th>
                    <th>Fulfillment</th>
                    <th>Payment</th>
                    <th>Total</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  {(data?.data ?? [])
                    .filter(c =>
                      !search ||
                      `${c.given_name} ${c.last_name}`.toLowerCase().includes(search.toLowerCase()) ||
                      c.email.toLowerCase().includes(search.toLowerCase())
                    )
                    .map((c) => (
                      <tr key={c.customer_id}>
                        <td style={{ color: "var(--text-muted)" }}>#{c.customer_id}</td>
                        <td style={{ fontWeight: 600 }}>
                          {c.given_name} {c.middle_name ? c.middle_name[0] + "." : ""} {c.last_name} {c.suffix ?? ""}
                        </td>
                        <td style={{ fontSize: 12, color: "var(--text-muted)" }}>
                          {new Date(c.created_at).toLocaleDateString("en-PH")}
                        </td>
                        <td>{c.email}</td>
                        <td>{c.contact_num ?? "—"}</td>
                        <td>—</td>
                        <td>—</td>
                      </tr>
                    ))}
                  {(data?.data ?? []).length === 0 && (
                    <tr>
                      <td colSpan={7}>
                        <div className="empty-state"><p>No customers found</p></div>
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
            {data && data.total > 20 && (
              <div style={{ display: "flex", gap: 8, justifyContent: "flex-end", marginTop: 16 }}>
                <button className="btn btn-secondary" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</button>
                <span style={{ lineHeight: "36px", fontSize: 12, color: "var(--text-muted)" }}>Page {page}</span>
                <button className="btn btn-secondary" disabled={page * 20 >= data.total} onClick={() => setPage(p => p + 1)}>Next →</button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}

function CustomerForm({ onClose, onSaved }: { onClose: () => void; onSaved: () => void }) {
  const [form, setForm] = useState({
    last_name: "", given_name: "", middle_name: "", suffix: "",
    email: "", contact_num: "",
  });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  const handleSave = async () => {
    if (!form.last_name || !form.given_name || !form.email) {
      setErr("Last name, given name and email are required."); return;
    }
    setSaving(true);
    try {
      await customersApi.create(form);
      onSaved(); onClose();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  const f = (key: keyof typeof form) => ({
    className: "form-input",
    value: form[key],
    onChange: (e: React.ChangeEvent<HTMLInputElement>) => setForm({ ...form, [key]: e.target.value }),
  });

  return (
    <div style={overlay}>
      <div style={modal}>
        <h3 style={{ marginBottom: 16, fontSize: 16 }}>New Customer</h3>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
            <div className="form-group"><label className="form-label">Given Name *</label><input {...f("given_name")} /></div>
            <div className="form-group"><label className="form-label">Last Name *</label><input {...f("last_name")} /></div>
            <div className="form-group"><label className="form-label">Middle Name</label><input {...f("middle_name")} /></div>
            <div className="form-group"><label className="form-label">Suffix</label><input {...f("suffix")} placeholder="Jr., Sr., III" /></div>
          </div>
          <div className="form-group"><label className="form-label">Email *</label><input {...f("email")} type="email" /></div>
          <div className="form-group"><label className="form-label">Contact Number</label><input {...f("contact_num")} placeholder="09xxxxxxxxx" /></div>
          {err && <p style={{ color: "#c0392b", fontSize: 12 }}>{err}</p>}
          <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
            <button className="btn btn-secondary" onClick={onClose}>Cancel</button>
            <button className="btn btn-primary" onClick={handleSave} disabled={saving}>{saving ? "Saving…" : "Save"}</button>
          </div>
        </div>
      </div>
    </div>
  );
}

const overlay: React.CSSProperties = { position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 200 };
const modal: React.CSSProperties = { background: "#fff", borderRadius: 14, padding: 28, width: "100%", maxWidth: 500 };
