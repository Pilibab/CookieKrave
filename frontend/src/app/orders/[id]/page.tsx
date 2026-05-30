"use client";

import { useFetch, useMutation } from "@/hooks/useFetch";
import { ordersApi } from "@/lib/api";
import { useParams } from "next/navigation";
import Link from "next/link";
import type { OrderStatus } from "@/types";

const STATUS_FLOW: OrderStatus[] = [
  "Out for Delivery", "Confirmed", "Pending", "Baking", "Completed",
];

export default function OrderDetailPage() {
  const { id } = useParams<{ id: string }>();
  const orderId = Number(id);

  const { data: order, loading, error, refetch } = useFetch(
    () => ordersApi.get(orderId),
    [orderId]
  );

  const { mutate: updateStatus, loading: updating } = useMutation(
    (status: OrderStatus) => ordersApi.updateStatus(orderId, status)
  );

  const handleStatusChange = async (status: OrderStatus) => {
    await updateStatus(status);
    refetch();
  };

  if (loading) return <div><div className="spinner" /></div>;
  if (error || !order) return <div><p style={{ color: "red" }}>Order not found.</p></div>;

  const allStatuses: OrderStatus[] = ["Out for Delivery", "Confirmed", "Pending", "Baking", "Completed"];

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <Link href="/orders" style={{ fontSize: 13, color: "var(--text-muted)" }}>← Orders</Link>
          <h1 className="page-title" style={{ color: "var(--navy)" }}>Order#{order.order_id}</h1>
        </div>
      </div>

      {/* Status buttons row */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: 24 }}>
        {allStatuses.map((status) => {
          const isActive = order.order_status === status;
          return (
            <button
              key={status}
              onClick={() => handleStatusChange(status)}
              disabled={updating}
              style={{
                padding: "7px 16px",
                borderRadius: 20,
                fontSize: 13,
                fontWeight: 600,
                cursor: updating ? "not-allowed" : "pointer",
                border: isActive ? "none" : "1.5px solid var(--border)",
                background: isActive ? "var(--navy)" : "var(--warm-white)",
                color: isActive ? "#fff" : "var(--text)",
                transition: "all 0.15s",
              }}
            >
              {status}
            </button>
          );
        })}
      </div>

      {/* Customer & Fulfillment side by side */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
        {/* Customer */}
        <div className="card">
          <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 16, color: "var(--text-muted)" }}>Customer</h3>
          {order.customer ? (
            <dl style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 13 }}>
              <div style={{ display: "flex", gap: 12 }}>
                <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 60 }}>Name</dt>
                <dd style={{ fontWeight: 500 }}>{order.customer.given_name} {order.customer.middle_name ?? ""} {order.customer.last_name} {order.customer.suffix ?? ""}</dd>
              </div>
              <div style={{ display: "flex", gap: 12 }}>
                <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 60 }}>Email</dt>
                <dd>{order.customer.email}</dd>
              </div>
              <div style={{ display: "flex", gap: 12 }}>
                <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 60 }}>Contact</dt>
                <dd>{order.customer.contact_num ?? "—"}</dd>
              </div>
            </dl>
          ) : <p style={{ color: "var(--text-muted)", fontSize: 13 }}>Customer #{order.customer_id}</p>}
        </div>

        {/* Fulfillment */}
        <div className="card">
          <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 16, color: "var(--text-muted)" }}>Fulfillment</h3>
          <dl style={{ display: "flex", flexDirection: "column", gap: 10, fontSize: 13 }}>
            <div style={{ display: "flex", gap: 12 }}>
              <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 70 }}>Type</dt>
              <dd>{order.fulfillment?.fulfillment_type ?? "—"}</dd>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 70 }}>Address</dt>
              <dd>{order.fulfillment?.fulfillment_type === "Delivery" && order.fulfillment.delivery
                ? order.fulfillment.delivery.address
                : "—"}</dd>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 70 }}>Payment</dt>
              <dd>{order.payment_method}</dd>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <dt style={{ color: "var(--text-muted)", fontWeight: 500, minWidth: 70 }}>Total</dt>
              <dd style={{ fontWeight: 700 }}>₱{Number(order.total_amount).toLocaleString("en-PH", { minimumFractionDigits: 2 })}</dd>
            </div>
          </dl>
        </div>
      </div>

      {/* Ordered items */}
      {(order.cart_items ?? []).length > 0 && (
        <div className="card" style={{ marginTop: 16 }}>
          <h3 style={{ fontSize: 14, fontWeight: 700, marginBottom: 14 }}>Ordered Items</h3>
          <table>
            <thead>
              <tr>
                <th>Product</th>
                <th>Price/Item</th>
                <th>Qty</th>
                <th>Subtotal</th>
              </tr>
            </thead>
            <tbody>
              {(order.cart_items ?? []).map((item) => (
                <tr key={item.product_id}>
                  <td>{item.product?.product_name ?? `Product #${item.product_id}`}</td>
                  <td>₱{Number(item.price_per_item).toFixed(2)}</td>
                  <td>{item.quantity}</td>
                  <td style={{ fontWeight: 600 }}>₱{(item.price_per_item * item.quantity).toLocaleString("en-PH", { minimumFractionDigits: 2 })}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
