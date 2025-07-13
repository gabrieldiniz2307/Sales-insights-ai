-- Criando o esquema do banco
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sku VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10, 2)
);

CREATE TABLE customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER REFERENCES products(id),
    customer_id INTEGER REFERENCES customers(id),
    quantity INTEGER NOT NULL,
    total_amount NUMERIC(10, 2) NOT NULL,
    sale_date TIMESTAMP NOT NULL
);

-- Inserindo dados na tabela products
INSERT INTO products (sku, name, category, price) VALUES ('SKU001', 'Smartphone Galaxy S21', 'Eletrônicos', 1500.00);
INSERT INTO products (sku, name, category, price) VALUES ('SKU002', 'Notebook Dell Inspiron', 'Informática', 2800.00);
INSERT INTO products (sku, name, category, price) VALUES ('SKU003', 'Fone Bluetooth Sony', 'Eletrônicos', 350.00);
INSERT INTO products (sku, name, category, price) VALUES ('SKU004', 'Mouse Gamer Logitech', 'Informática', 180.00);
INSERT INTO products (sku, name, category, price) VALUES ('SKU005', 'Teclado Mecânico RGB', 'Informática', 450.00);

-- Inserindo dados na tabela customers
INSERT INTO customers (name, email) VALUES ('João Silva', 'joao@email.com');
INSERT INTO customers (name, email) VALUES ('Maria Santos', 'maria@email.com');
INSERT INTO customers (name, email) VALUES ('Pedro Oliveira', 'pedro@email.com');
INSERT INTO customers (name, email) VALUES ('Ana Costa', 'ana@email.com');
INSERT INTO customers (name, email) VALUES ('Carlos Ferreira', 'carlos@email.com');

-- Inserindo dados na tabela sales com datas dos últimos 30 dias
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 1, 2, 3000.00, '2025-07-10 10:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 2, 1, 2800.00, '2025-07-09 14:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 3, 3, 1050.00, '2025-07-08 16:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 4, 5, 900.00, '2025-07-07 09:15:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 5, 2, 900.00, '2025-07-06 11:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 2, 1, 1500.00, '2025-07-05 15:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 3, 1, 2800.00, '2025-07-04 13:10:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 4, 2, 700.00, '2025-07-03 17:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 5, 3, 540.00, '2025-07-02 12:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 1, 1, 450.00, '2025-07-01 10:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 3, 3, 4500.00, '2025-06-30 14:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 4, 2, 5600.00, '2025-06-29 16:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 5, 4, 1400.00, '2025-06-28 11:15:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 1, 6, 1080.00, '2025-06-27 09:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 2, 3, 1350.00, '2025-06-26 15:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 4, 1, 1500.00, '2025-06-25 13:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 5, 1, 2800.00, '2025-06-24 17:10:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 1, 5, 1750.00, '2025-06-23 12:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 2, 4, 720.00, '2025-06-22 14:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 3, 2, 900.00, '2025-06-21 16:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 5, 2, 3000.00, '2025-06-20 10:15:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 1, 1, 2800.00, '2025-06-19 11:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 2, 3, 1050.00, '2025-06-18 15:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 3, 7, 1260.00, '2025-06-17 13:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 4, 4, 1800.00, '2025-06-16 17:00:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 2, 1, 1500.00, '2025-06-15 09:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 3, 2, 5600.00, '2025-06-14 12:15:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 4, 6, 2100.00, '2025-06-13 14:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 5, 8, 1440.00, '2025-06-12 16:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 1, 5, 2250.00, '2025-06-11 11:00:00');

-- Adicionando mais vendas para o último mês (junho-julho 2025)
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 3, 4, 6000.00, '2025-07-11 08:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 4, 2, 3000.00, '2025-07-12 10:15:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (1, 5, 3, 4500.00, '2025-07-13 09:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (2, 1, 3, 8400.00, '2025-07-11 14:20:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (3, 2, 8, 2800.00, '2025-07-12 16:30:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (4, 3, 12, 2160.00, '2025-07-13 11:45:00');
INSERT INTO sales (product_id, customer_id, quantity, total_amount, sale_date) VALUES (5, 4, 6, 2700.00, '2025-07-11 13:00:00');

