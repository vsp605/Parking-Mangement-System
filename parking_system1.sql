CREATE DATABASE IF NOT EXISTS parking_system1;

USE parking_system1;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    avatar VARCHAR(255)
);
USE parking_system1;

CREATE TABLE notifications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
USE parking_system1;

INSERT INTO notifications (message) VALUES 
('Your parking slot has been booked successfully.'),
('Payment has been processed successfully.'),
('Your booking has been canceled.'),
('Your parking time is about to expire.'),
('New parking slots are now available.'),
('System maintenance scheduled for midnight.'),
('You have a new notification from the admin.'),
('Your payment receipt has been emailed.'),
('A new feature has been added to the system.'),
('Reminder: Update your account details.');


USE parking_system1;

CREATE TABLE ParkingSlot (
    id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    slot_number INT NOT NULL,
    status VARCHAR(20) DEFAULT 'available',
    user_id INT DEFAULT NULL
);
USE parking_system1;

SELECT id, location, slot_number, status FROM ParkingSlot WHERE location = 'NAVANAGAR';
SHOW DATABASES;
DESCRIBE payments;
ALTER TABLE payments ADD COLUMN user_id INT NOT NULL;

-- Insert initial slots for different locations
INSERT INTO ParkingSlot (location, slot_number) VALUES
('BAGALKOT', 1), ('BAGALKOT', 2), ('BAGALKOT', 3), ('BAGALKOT', 4), ('BAGALKOT', 5),
('BAGALKOT', 6), ('BAGALKOT', 7), ('BAGALKOT', 8), ('BAGALKOT', 9), ('BAGALKOT', 10),
('BAGALKOT', 11), ('BAGALKOT', 12), ('BAGALKOT', 13), ('BAGALKOT', 14), ('BAGALKOT', 15),
('BAGALKOT', 16), ('BAGALKOT', 17), ('BAGALKOT', 18), ('BAGALKOT', 19), ('BAGALKOT', 20),
('CHANDAN THEATER', 1), ('CHANDAN THEATER', 2), ('CHANDAN THEATER', 3), ('CHANDAN THEATER', 4), ('CHANDAN THEATER', 5),
('CHANDAN THEATER', 6), ('CHANDAN THEATER', 7), ('CHANDAN THEATER', 8), ('CHANDAN THEATER', 9), ('CHANDAN THEATER', 10),
('CHANDAN THEATER', 11), ('CHANDAN THEATER', 12), ('CHANDAN THEATER', 13), ('CHANDAN THEATER', 14), ('CHANDAN THEATER', 15),
('CHANDAN THEATER', 16), ('CHANDAN THEATER', 17), ('CHANDAN THEATER', 18), ('CHANDAN THEATER', 19), ('CHANDAN THEATER', 20),
('NAVANAGAR', 1), ('NAVANAGAR', 2), ('NAVANAGAR', 3), ('NAVANAGAR', 4), ('NAVANAGAR', 5),
('NAVANAGAR', 6), ('NAVANAGAR', 7), ('NAVANAGAR', 8), ('NAVANAGAR', 9), ('NAVANAGAR', 10),
('NAVANAGAR', 11), ('NAVANAGAR', 12), ('NAVANAGAR', 13), ('NAVANAGAR', 14), ('NAVANAGAR', 15),
('NAVANAGAR', 16), ('NAVANAGAR', 17), ('NAVANAGAR', 18), ('NAVANAGAR', 19), ('NAVANAGAR', 20);

USE parking_system1;

CREATE TABLE Payment1 (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);


USE parking_system1;

CREATE TABLE parking_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    slot_number INT NOT NULL,
    status ENUM('available', 'booked') DEFAULT 'available'
);

-- Insert some default slots
INSERT INTO parking_slots (slot_number, status)
VALUES (1, 'available'), (2, 'available'), (3, 'available'), (4, 'available'), (5, 'available'),
       (6, 'available'), (7, 'available'), (8, 'available'), (9, 'available'), (10, 'available'),
       (11, 'available'), (12, 'available'), (13, 'available'), (14, 'available'), (15, 'available'),
       (16, 'available'), (17, 'available'), (18, 'available'), (19, 'available'), (20, 'available');




USE parking_system1;

CREATE TABLE payments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    plot_no VARCHAR(50) NOT NULL,
    vehicle_no VARCHAR(50) NOT NULL,
    vehicle_type VARCHAR(20) NOT NULL,
    hours INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    payment_type VARCHAR(20) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



USE parking_system1;

CREATE TABLE Bill (
    bill_id VARCHAR(50) PRIMARY KEY,
    payment_id VARCHAR(50) NOT NULL,
    slot_id VARCHAR(50) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    bill_date DATE NOT NULL
);
USE parking_system1;
CREATE TABLE admin_users (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(200) NOT NULL
);

USE parking_system1;

CREATE TABLE parking_slots1 (
    slot_id INT AUTO_INCREMENT PRIMARY KEY,
    location VARCHAR(100) NOT NULL,
    slot_number INT NOT NULL,
    status VARCHAR(20) DEFAULT 'available'  -- available or booked
);

