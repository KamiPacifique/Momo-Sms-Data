CREATE DATABASE IF NOT EXISTS momo_sms_db;
USE momo_sms_db;

-- CREATE TABLES

CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    phone_number VARCHAR(15) UNIQUE NOT NULL,
    id_number VARCHAR(16) NOT NULL,
    registration_date DATETIME NOT NULL,
    status VARCHAR(20) DEFAULT 'ACTIVE',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transaction_categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(50) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE transactions (
    transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT DEFAULT NULL,
    category_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL CHECK (amount >= 0),
    currency CHAR(3) DEFAULT 'RWF',
    transaction_type VARCHAR(50),
    transaction_status ENUM('SUCCESS','PENDING','FAILED','REVERSED') NOT NULL DEFAULT 'PENDING',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_transactions_sender
        FOREIGN KEY (sender_id) REFERENCES users(user_id)
        ON DELETE RESTRICT ON UPDATE CASCADE,

    CONSTRAINT fk_transactions_receiver
        FOREIGN KEY (receiver_id) REFERENCES users(user_id)
        ON DELETE SET NULL ON UPDATE CASCADE,

    CONSTRAINT fk_transactions_category
        FOREIGN KEY (category_id) REFERENCES transaction_categories(category_id)
        ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE tags (
    tag_id INT AUTO_INCREMENT PRIMARY KEY,
    tag_name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    UNIQUE (tag_name)
);

CREATE TABLE transaction_tags (
    transaction_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (transaction_id, tag_id),

    CONSTRAINT fk_tt_transaction
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        ON DELETE CASCADE ON UPDATE CASCADE,

    CONSTRAINT fk_tt_tag
        FOREIGN KEY (tag_id) REFERENCES tags(tag_id)
        ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE system_logs (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT DEFAULT NULL,
    action VARCHAR(20) NOT NULL,
    log_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    status_message VARCHAR(255),

    CONSTRAINT fk_log_transaction
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        ON DELETE SET NULL ON UPDATE CASCADE
);


-- CREATE INDEXES
CREATE INDEX idx_transactions_sender_date ON transactions (sender_id, created_at);
CREATE INDEX idx_transactions_receiver_date ON transactions (receiver_id, created_at);
CREATE INDEX idx_transactions_category ON transactions (category_id);
CREATE INDEX idx_transactions_status_date ON transactions (transaction_status, created_at);
CREATE INDEX idx_transaction_tags_tag ON transaction_tags (tag_id, transaction_id);
CREATE INDEX idx_system_logs_txn_time ON system_logs (transaction_id, log_time);


-- SECURITY & DATA VALIDATION CONSTRAINTS

ALTER TABLE users ADD CONSTRAINT unique_id_number UNIQUE (id_number);
ALTER TABLE transaction_categories ADD CONSTRAINT unique_category_name UNIQUE (category_name);
ALTER TABLE users ADD CONSTRAINT chk_phone_format CHECK (phone_number REGEXP '^\\+250[0-9]{9}$');
ALTER TABLE users ADD CONSTRAINT chk_id_number_format CHECK (id_number REGEXP '^[0-9]{16}$');
ALTER TABLE users ADD CONSTRAINT chk_user_status CHECK (status IN ('ACTIVE', 'INACTIVE', 'SUSPENDED', 'PENDING_VERIFICATION'));
ALTER TABLE transactions ADD CONSTRAINT chk_amount_positive CHECK (amount > 0);
ALTER TABLE transactions ADD CONSTRAINT chk_transaction_type CHECK (transaction_type IN ('P2P_TRANSFER', 'CASH_OUT', 'BILL_PAYMENT', 'AIRTIME', 'MERCHANT_PAY', 'DEPOSIT'));
ALTER TABLE transactions ADD CONSTRAINT chk_amount_limit CHECK (amount <= 10000000);

-- INSERT SAMPLE DATA

INSERT INTO users (full_name, phone_number, id_number, registration_date, status, created_at) VALUES
('Arsene Hirwa', '+250788312567', '1199980183047290', '2024-09-10 10:15:00', 'ACTIVE', '2024-09-10 10:15:00'),
('Vanesa Rusengwa', '+250784031874', '1200570326821437', '2024-10-20 09:45:00', 'SUSPENDED', '2024-10-20 09:45:00'),
('Christa Ishimwe', '+250791324921', '1200270514904172', '2024-11-02 11:20:00', 'ACTIVE', '2024-11-02 11:20:00'),
('Ank Micha', '+250793252350', '1200070226340695', '2024-08-12 12:00:00', 'ACTIVE', '2024-08-12 12:00:00'),
('Axel Iragaba', '+250790558929', '1200380438625309', '2024-12-15 08:00:00', 'ACTIVE', '2024-12-15 08:00:00'),
('Abigael Kagabo', '+250794223408', '1199880870122456', '2025-01-02 07:00:00', 'ACTIVE', '2025-01-02 07:00:00');

INSERT INTO transaction_categories (category_name, description) VALUES
('CASH_OUT', 'Withdraw money from MoMo account'),
('DEPOSIT', 'Deposit money into MoMo account'),
('SEND_MONEY', 'Transfer money to another MoMo user'),
('AIRTIME_TOPUP', 'Purchase mobile airtime'),
('PAY_BILL', 'Payment for services'),
('INTERNATIONAL_TRANSFER', 'Cross border money transfer'),
('MERCHANT_PAYMENT', 'Payment to registered merchant');

INSERT INTO transactions (sender_id, receiver_id, category_id, amount, currency, transaction_type, transaction_status, created_at) VALUES
(1, 2, 3, 6000.00, 'RWF', 'P2P_TRANSFER', 'SUCCESS', '2025-01-10 14:30:00'),
(2, 3, 1, 30000.00, 'RWF', 'CASH_OUT', 'SUCCESS', '2024-12-20 10:20:00'),
(3, NULL, 5, 10000.00, 'RWF', 'BILL_PAYMENT', 'FAILED', '2025-01-13 08:20:00'),
(4, 5, 3, 85000.00, 'RWF', 'P2P_TRANSFER', 'PENDING', '2025-01-20 12:00:00'),
(5, 1, 4, 1000.00, 'RWF', 'AIRTIME', 'SUCCESS', '2025-01-22 09:00:00'),
(6, 4, 7, 40000.00, 'RWF', 'MERCHANT_PAY', 'SUCCESS', '2025-01-18 10:00:00'),
(1, 3, 7, 20000.00, 'RWF', 'MERCHANT_PAY', 'FAILED', '2025-01-19 11:00:00'),
(2, NULL, 1, 60000.00, 'RWF', 'CASH_OUT', 'REVERSED', '2025-01-20 15:20:00');

INSERT INTO tags (tag_name, description) VALUES
('FRAUD_SUSPECTED', 'Transaction flagged for fraud review'),
('HIGH_VALUE', 'Transaction above threshold amount'),
('RECURRING', 'Regular repeating transaction'),
('URGENT', 'Time-sensitive transaction'),
('INTERNATIONAL', 'Cross-border transaction'),
('BUSINESS', 'Commercial transaction'),
('PERSONAL', 'Personal transaction');

INSERT INTO transaction_tags (transaction_id, tag_id) VALUES
(1, 7),
(2, 7),
(3, 1),
(4, 2), (4, 7),
(5, 7),
(6, 6),
(7, 1), (7, 6),
(8, 2), (8, 7);

INSERT INTO system_logs (transaction_id, action, log_time, status_message) VALUES
(1, 'INITIATE', '2025-01-10 14:30:05', 'Transaction initiated successfully'),
(1, 'COMPLETE', '2025-01-10 14:31:00', 'Transaction processed successfully'),
(2, 'REQUEST', '2024-12-20 10:20:05', 'Cash out request received'),
(2, 'COMPLETE', '2024-12-20 10:21:00', 'Cash out completed at agent location'),
(3, 'INITIATE', '2025-01-13 08:20:05', 'Bill payment initiated'),
(3, 'FAILED', '2025-01-13 08:21:00', 'Payment failed - insufficient funds'),
(4, 'INITIATE', '2025-01-20 12:00:05', 'Transfer initiated'),
(4, 'PENDING', '2025-01-20 12:01:00', 'Waiting for receiver confirmation'),
(5, 'REQUEST', '2025-01-22 09:00:05', 'Airtime purchase requested'),
(5, 'COMPLETE', '2025-01-22 09:01:00', 'Airtime credited successfully'),
(6, 'INITIATE', '2025-01-18 10:00:05', 'Merchant payment initiated'),
(6, 'COMPLETE', '2025-01-18 10:01:00', 'Payment to merchant completed'),
(7, 'INITIATE', '2025-01-19 11:00:05', 'Merchant payment initiated'),
(7, 'FAILED', '2025-01-19 11:01:00', 'Transaction declined by merchant'),
(8, 'REQUEST', '2025-01-20 15:20:05', 'Cash out request received'),
(8, 'REVERSED', '2025-01-20 15:21:00', 'Transaction reversed - duplicate request');
