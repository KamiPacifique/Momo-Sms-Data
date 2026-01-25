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
