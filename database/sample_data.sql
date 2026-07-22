-- =====================================================
-- Sample Data
-- =====================================================
USE online_shopping;

-- Admin user (password: admin123 -> hashed with werkzeug in app; placeholder hash below
-- will be replaced automatically the first time you run backend/seed.py)
INSERT INTO Users (full_name, email, password_hash, phone, address, role) VALUES
('Site Admin', 'admin@shop.com', 'PLACEHOLDER', '9999999999', 'Head Office', 'admin'),
('John Doe', 'john@example.com', 'PLACEHOLDER', '9876543210', '12 Main St, Chennai', 'customer'),
('Jane Smith', 'jane@example.com', 'PLACEHOLDER', '9876500000', '45 Park Ave, Bengaluru', 'customer');

INSERT INTO Categories (category_name, description) VALUES
('Electronics', 'Phones, laptops, gadgets'),
('Fashion', 'Clothing and accessories'),
('Home & Kitchen', 'Appliances and kitchenware'),
('Books', 'Fiction and non-fiction books');

INSERT INTO Products (product_name, description, price, stock_quantity, category_id, image_url) VALUES
('Wireless Mouse', 'Ergonomic 2.4GHz wireless mouse', 599.00, 50, 1, 'mouse.jpg'),
('Bluetooth Headphones', 'Over-ear noise cancelling headphones', 2499.00, 30, 1, 'headphones.jpg'),
('Men''s Cotton T-Shirt', 'Comfortable round-neck t-shirt', 399.00, 100, 2, 'tshirt.jpg'),
('Non-Stick Frying Pan', '28cm non-stick frying pan', 899.00, 40, 3, 'pan.jpg'),
('The Pragmatic Programmer', 'Popular software engineering book', 1200.00, 25, 4, 'book.jpg'),
('Smartphone Stand', 'Adjustable aluminum phone stand', 299.00, 60, 1, 'stand.jpg');

INSERT INTO Reviews (product_id, user_id, rating, comment) VALUES
(1, 2, 5, 'Great mouse, very responsive.'),
(1, 3, 4, 'Good value for money.'),
(2, 2, 4, 'Sound quality is excellent.'),
(5, 3, 5, 'A must-read for developers.');
