CREATE TABLE gcash_payments (
  ord_id      INT PRIMARY KEY REFERENCES orders(ord_id) ON DELETE CASCADE,
  reference_no  VARCHAR(50) NOT NULL,
  amount        NUMERIC(7,2) NOT NULL,
  paid_at       TIMESTAMPTZ DEFAULT NOW()
);