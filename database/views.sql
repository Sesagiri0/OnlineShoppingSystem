-- =====================================================
-- Views
-- =====================================================
USE online_shopping;

DROP VIEW IF EXISTS ProductDetails;
DROP VIEW IF EXISTS CustomerOrders;

-- Product details joined with category and average rating
CREATE VIEW ProductDetails AS
SELECT
    p.product_id,
    p.product_name,
    p.description,
    p.price,
    p.stock_quantity,
    c.category_name,
    COALESCE(AVG(r.rating), 0) AS average_rating,
    COUNT(r.review_id) AS review_count
FROM Products p
LEFT JOIN Categories c ON p.category_id = c.category_id
LEFT JOIN Reviews r ON p.product_id = r.product_id
GROUP BY p.product_id, p.product_name, p.description, p.price,
         p.stock_quantity, c.category_name;

-- Customer order summary (uses INNER JOIN + LEFT JOIN)
CREATE VIEW CustomerOrders AS
SELECT
    u.user_id,
    u.full_name,
    u.email,
    o.order_id,
    o.order_date,
    o.status,
    o.total_amount,
    pay.payment_method,
    pay.payment_status
FROM Users u
INNER JOIN Orders o ON u.user_id = o.user_id
LEFT JOIN Payments pay ON o.order_id = pay.order_id;
