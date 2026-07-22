-- =====================================================
-- Triggers
-- =====================================================
USE online_shopping;

DROP TRIGGER IF EXISTS trg_reduce_stock_after_order;
DROP TRIGGER IF EXISTS trg_prevent_negative_stock;
DROP TRIGGER IF EXISTS trg_update_order_after_payment;

DELIMITER //

-- 1. Reduce stock automatically after an item is added to an order
CREATE TRIGGER trg_reduce_stock_after_order
AFTER INSERT ON OrderItems
FOR EACH ROW
BEGIN
    UPDATE Products
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE product_id = NEW.product_id;
END //

-- 2. Prevent stock from ever going negative
CREATE TRIGGER trg_prevent_negative_stock
BEFORE UPDATE ON Products
FOR EACH ROW
BEGIN
    IF NEW.stock_quantity < 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Stock cannot be negative';
    END IF;
END //

-- 3. Automatically update order status once payment is completed
CREATE TRIGGER trg_update_order_after_payment
AFTER UPDATE ON Payments
FOR EACH ROW
BEGIN
    IF NEW.payment_status = 'Completed' AND OLD.payment_status <> 'Completed' THEN
        UPDATE Orders
        SET status = 'Processing'
        WHERE order_id = NEW.order_id;
    END IF;
END //

DELIMITER ;
