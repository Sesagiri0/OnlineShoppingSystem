-- =====================================================
-- Indexes for faster search & reporting
-- =====================================================
USE online_shopping;

CREATE INDEX idx_product_name ON Products(product_name);
CREATE INDEX idx_product_category ON Products(category_id);
CREATE INDEX idx_order_date ON Orders(order_date);
CREATE INDEX idx_user_email ON Users(email);
