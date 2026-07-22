-- =====================================================
-- Functions
-- =====================================================
USE online_shopping;

DROP FUNCTION IF EXISTS CalculateDiscount;
DROP FUNCTION IF EXISTS CalculateGST;
DROP FUNCTION IF EXISTS TotalOrderAmount;

DELIMITER //

-- Returns discounted price given original price and discount %
CREATE FUNCTION CalculateDiscount(p_price DECIMAL(10,2), p_discount_percent DECIMAL(5,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN ROUND(p_price - (p_price * p_discount_percent / 100), 2);
END //

-- Returns GST/tax amount for a given price and tax rate (default 18%)
CREATE FUNCTION CalculateGST(p_price DECIMAL(10,2), p_gst_rate DECIMAL(5,2))
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    RETURN ROUND(p_price * p_gst_rate / 100, 2);
END //

-- Returns the total bill amount (items + GST) for a given order
CREATE FUNCTION TotalOrderAmount(p_order_id INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_subtotal DECIMAL(10,2);
    SELECT COALESCE(SUM(quantity * unit_price), 0) INTO v_subtotal
    FROM OrderItems WHERE order_id = p_order_id;

    RETURN v_subtotal + CalculateGST(v_subtotal, 18);
END //

DELIMITER ;
