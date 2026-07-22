-- =====================================================
-- Stored Procedures
-- =====================================================
USE online_shopping;

DROP PROCEDURE IF EXISTS AddProduct;
DROP PROCEDURE IF EXISTS PlaceOrder;
DROP PROCEDURE IF EXISTS UpdateStock;
DROP PROCEDURE IF EXISTS SalesReport;

DELIMITER //

-- Add a new product
CREATE PROCEDURE AddProduct (
    IN p_name VARCHAR(150),
    IN p_description TEXT,
    IN p_price DECIMAL(10,2),
    IN p_stock INT,
    IN p_category_id INT,
    IN p_image_url VARCHAR(255)
)
BEGIN
    INSERT INTO Products (product_name, description, price, stock_quantity, category_id, image_url)
    VALUES (p_name, p_description, p_price, p_stock, p_category_id, p_image_url);
END //

-- Place an order: creates order header + moves cart items (passed as JSON) - simplified
-- Here we place an order for a single product/quantity; the Flask app loops this per cart item
-- inside a transaction, then updates the order total.
CREATE PROCEDURE PlaceOrder (
    IN p_user_id INT,
    IN p_product_id INT,
    IN p_quantity INT,
    IN p_shipping_address VARCHAR(255),
    OUT p_order_id INT
)
BEGIN
    DECLARE v_price DECIMAL(10,2);
    DECLARE v_stock INT;

    SELECT price, stock_quantity INTO v_price, v_stock
    FROM Products WHERE product_id = p_product_id FOR UPDATE;

    IF v_stock < p_quantity THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Insufficient stock for product';
    END IF;

    -- Reuse an existing pending order for this user created in the last 5 minutes, else create one
    SELECT order_id INTO p_order_id FROM Orders
    WHERE user_id = p_user_id AND status = 'Pending'
      AND order_date >= (NOW() - INTERVAL 5 MINUTE)
    ORDER BY order_id DESC LIMIT 1;

    IF p_order_id IS NULL THEN
        INSERT INTO Orders (user_id, status, total_amount, shipping_address)
        VALUES (p_user_id, 'Pending', 0, p_shipping_address);
        SET p_order_id = LAST_INSERT_ID();
    END IF;

    INSERT INTO OrderItems (order_id, product_id, quantity, unit_price)
    VALUES (p_order_id, p_product_id, p_quantity, v_price);

    UPDATE Orders
    SET total_amount = (
        SELECT SUM(quantity * unit_price) FROM OrderItems WHERE order_id = p_order_id
    )
    WHERE order_id = p_order_id;
END //

-- Update stock manually (e.g. restock by admin)
CREATE PROCEDURE UpdateStock (
    IN p_product_id INT,
    IN p_quantity_change INT
)
BEGIN
    UPDATE Products
    SET stock_quantity = stock_quantity + p_quantity_change
    WHERE product_id = p_product_id;
END //

-- Generate a sales report between two dates
CREATE PROCEDURE SalesReport (
    IN p_start_date DATE,
    IN p_end_date DATE
)
BEGIN
    SELECT
        DATE(o.order_date) AS sale_date,
        COUNT(DISTINCT o.order_id) AS total_orders,
        SUM(oi.quantity) AS total_units_sold,
        SUM(oi.quantity * oi.unit_price) AS total_revenue
    FROM Orders o
    JOIN OrderItems oi ON o.order_id = oi.order_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
      AND o.status <> 'Cancelled'
    GROUP BY DATE(o.order_date)
    ORDER BY sale_date;
END //

DELIMITER ;
