"use client";

import { useState } from "react";
import { useFetch } from "@/hooks/useFetch";
import { inventoryApi } from "@/lib/api";
import type { InventoryItem } from "@/types";

const FILTERS = ["All", "Pending", "Preparing", "Ready"];

export default function InventoryPage() {
  const { data: items, loading, refetch } = useFetch(inventoryApi.list);
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState<InventoryItem | null>(null);
  const [activeFilter, setActiveFilter] = useState("All");

  const isLow = (item: InventoryItem) => item.current_stock <= item.recorder_trigger;
  const isCritical = (item: InventoryItem) => item.current_stock <= item.recorder_trigger * 0.5;

  const lowItems = (items ?? []).filter(isLow);
  const lowNames = lowItems.slice(0, 2).map(i => i.ingredients_name).join(", ");

  const handleReorder = async (id: number) => {
    // Adjust stock to max level (recorder_trigger * 3 as default reorder qty)
    const item = (items ?? []).find(i => i.inventory_id === id);
    if (!item) return;
    await inventoryApi.adjustStock(id, item.recorder_trigger * 2);
    refetch();
  };

  const handleReorderAll = async () => {
    for (const item of (items ?? []).filter(isLow)) {
      await inventoryApi.adjustStock(item.inventory_id, item.recorder_trigger * 2);
    }
    refetch();
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title" style={{ color: "var(--navy)" }}>Inventory</h1>
          <p style={{ fontSize: 12, color: "var(--text-muted)", marginTop: 2 }}>
            {items?.length ?? 0} items
          </p>
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn btn-outline" style={{ background: "transparent", color: "var(--navy)", borderColor: "var(--navy)" }} onClick={handleReorderAll}>
            Reorder All
          </button>
          <button className="btn btn-primary" onClick={() => { setEditing(null); setShowForm(true); }}>
            + New Item
          </button>
        </div>
      </div>

      {showForm && (
        <InventoryForm initial={editing} onClose={() => setShowForm(false)} onSaved={refetch} />
      )}

      {/* Low stock alert banner */}
      {lowItems.length > 0 && (
        <div style={{
          background: "#fff1f0",
          border: "1px solid #fecaca",
          borderRadius: 12,
          padding: "12px 18px",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          marginBottom: 16,
          gap: 12,
        }}>
          <div style={{ display: "flex", alignItems: "center", gap: 10 }}>
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#c0392b" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/>
              <line x1="12" y1="9" x2="12" y2="13"/>
              <line x1="12" y1="17" x2="12.01" y2="17"/>
            </svg>
            <span style={{ fontSize: 13, color: "#c0392b", fontWeight: 600 }}>
              {lowItems.length} items below threshold: {lowNames}{lowItems.length > 2 ? "…" : ""}
            </span>
          </div>
          <button
            onClick={handleReorderAll}
            style={{
              background: "#c0392b", color: "#fff", border: "none",
              borderRadius: 8, padding: "6px 14px", fontSize: 12, fontWeight: 700, cursor: "pointer",
            }}
          >
            Reorder All
          </button>
        </div>
      )}

      {/* Filter pills */}
      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`status-btn${activeFilter === f ? " active" : ""}`}
            onClick={() => setActiveFilter(f)}
          >
            {f}
          </button>
        ))}
      </div>

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        {/* Status header inside card */}
        <div style={{ padding: "12px 24px", borderBottom: "1.5px solid var(--border)", display: "flex", justifyContent: "flex-end" }}>
          <span style={{ fontSize: 12, fontWeight: 600, color: "var(--text-muted)" }}>Status</span>
        </div>

        {loading && <div className="spinner" />}
        {!loading && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Item</th>
                  <th></th>
                  <th>Qty</th>
                  <th>Max</th>
                  <th>Reorder</th>
                  <th>Level</th>
                  <th>Category</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {(items ?? []).map((item) => {
                  const pct = item.current_stock / (item.recorder_trigger * 2 || 1) * 100;
                  const critical = isCritical(item);
                  const low = isLow(item);
                  return (
                    <tr key={item.inventory_id}>
                      <td style={{ fontWeight: 600, whiteSpace: "nowrap" }}>{item.ingredients_name}</td>
                      <td>
                        {/* Stock bar */}
                        <div className="stock-bar-bg" style={{ width: 120 }}>
                          <div
                            className={`stock-bar-fill${critical ? " critical" : ""}`}
                            style={{ width: `${Math.min(pct, 100)}%` }}
                          />
                        </div>
                      </td>
                      <td style={{ fontWeight: 600 }}>{item.current_stock} {item.unit_of_measure}</td>
                      <td style={{ color: "var(--text-muted)" }}>{item.recorder_trigger * 2}</td>
                      <td style={{ color: "var(--text-muted)" }}>{item.recorder_trigger}</td>
                      <td>
                        {critical ? (
                          <span className="badge-critical">● Critical</span>
                        ) : low ? (
                          <span style={{ color: "#e67e22", fontWeight: 700, fontSize: 12 }}>● Low</span>
                        ) : (
                          <span style={{ color: "#27ae60", fontWeight: 700, fontSize: 12 }}>● OK</span>
                        )}
                      </td>
                      <td style={{ color: "var(--text-muted)", fontSize: 12 }}>Ingredients</td>
                      <td>
                        <div style={{ display: "flex", gap: 6 }}>
                          <button
                            onClick={() => { setEditing(item); setShowForm(true); }}
                            style={{
                              background: "var(--cream)", border: "1px solid var(--border)",
                              borderRadius: 6, padding: "4px 8px", fontSize: 11, cursor: "pointer",
                            }}
                          >
                            ✎
                          </button>
                          <button
                            onClick={() => handleReorder(item.inventory_id)}
                            style={{
                              background: "#fde8e8", border: "1px solid #fecaca",
                              borderRadius: 6, padding: "4px 8px", fontSize: 11, cursor: "pointer", color: "#c0392b",
                            }}
                          >
                            ↺
                          </button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
                {(items ?? []).length === 0 && (
                  <tr>
                    <td colSpan={8}>
                      <div className="empty-state"><p>No inventory items</p></div>
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

function InventoryForm({
  initial, onClose, onSaved,
}: { initial: InventoryItem | null; onClose: () => void; onSaved: () => void }) {
  const [form, setForm] = useState({
    ingredients_name: initial?.ingredients_name ?? "",
    current_stock: initial?.current_stock ?? 0,
    unit_of_measure: initial?.unit_of_measure ?? "",
    recorder_trigger: initial?.recorder_trigger ?? 0,
  });
  const [saving, setSaving] = useState(false);
  const [err, setErr] = useState("");

  const handleSave = async () => {
    if (!form.ingredients_name || !form.unit_of_measure) { setErr("Name and unit are required."); return; }
    setSaving(true);
    try {
      if (initial) {
        await inventoryApi.update(initial.inventory_id, form);
      } else {
        await inventoryApi.create(form);
      }
      onSaved();
      onClose();
    } catch (e) {
      setErr(e instanceof Error ? e.message : "Save failed");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={overlay}>
      <div style={modal}>
        <h3 style={{ marginBottom: 16, fontSize: 16 }}>{initial ? "Edit Ingredient" : "New Ingredient"}</h3>
        <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
          <div className="form-group">
            <label className="form-label">Ingredient Name *</label>
            <input className="form-input" value={form.ingredients_name} onChange={(e) => setForm({ ...form, ingredients_name: e.target.value })} />
          </div>
          <div style={{ display: "flex", gap: 12 }}>
            <div className="form-group" style={{ flex: 1 }}>
              <label className="form-label">Current Stock</label>
              <input className="form-input" type="number" min={0} step={0.01} value={form.current_stock} onChange={(e) => setForm({ ...form, current_stock: Number(e.target.value) })} />
            </div>
            <div className="form-group" style={{ flex: 1 }}>
              <label className="form-label">Unit of Measure *</label>
              <input className="form-input" value={form.unit_of_measure} onChange={(e) => setForm({ ...form, unit_of_measure: e.target.value })} placeholder="e.g. grams, cups" />
            </div>
          </div>
          <div className="form-group">
            <label className="form-label">Reorder Trigger</label>
            <input className="form-input" type="number" min={0} value={form.recorder_trigger} onChange={(e) => setForm({ ...form, recorder_trigger: Number(e.target.value) })} />
          </div>
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

const overlay: React.CSSProperties = {
  position: "fixed", inset: 0, background: "rgba(0,0,0,0.45)",
  display: "flex", alignItems: "center", justifyContent: "center", zIndex: 200,
};
const modal: React.CSSProperties = {
  background: "#fff", borderRadius: 14, padding: 28, width: "100%", maxWidth: 460,
};
