CREATE DATABASE flight_booking;

USE flight_booking;

--------------------
#flightsTable
----------------------
CREATE TABLE flights(
    flight_id INT AUTO_INCREMENT PRIMARY KEY,
    airline_name VARCHAR(20),
    origin VARCHAR(20),
    destination VARCHAR(20),
    departure_time DATETIME,
    arrival_time DATETIME,
    total_seats INT,
    available_seats INT,
    base_price FLOAT
);


INSERT INTO flights 
(flight_id, airline_name, origin, destination, departure_time, arrival_time, total_seats, available_seats, base_price)
VALUES
(1, 'IndiGo', 'Hyderabad', 'Delhi', '2025-10-10 08:00:00', '2025-10-10 10:30:00', 180, 150, 3500.00),

(2, 'Air India', 'Mumbai', 'Chennai', '2025-10-11 09:15:00', '2025-10-11 11:45:00', 160, 140, 4200.00),

(3, 'SpiceJet', 'Bangalore', 'Kolkata', '2025-10-12 06:00:00', '2025-10-12 09:15:00', 150, 130, 3900.00),

(4, 'Vistara', 'Delhi', 'Goa', '2025-10-13 14:30:00', '2025-10-13 17:00:00', 200, 190, 4500.00),

(5, 'Akasa Air', 'Hyderabad', 'Pune', '2025-10-14 18:45:00', '2025-10-14 20:15:00', 170, 160, 2800.00);



--------------------
#passengersTable
----------------------

CREATE TABLE passengers(
    passenger_id INT AUTO_INCREMENT PRIMARY KEY,                       --PRIMARY KEY IS CONSTRAINT 
    name VARCHAR(50),
    age INT CHECK (age > 0),                                            --CHECK IS CONSTRAINT
    gender VARCHAR(20) CHECK (gender IN ('Male', 'Female', 'Other')),  --CHECK IS CONSTRAINT
    email VARCHAR(50) UNIQUE,                                           --UNIQUE IS CONSTRAINT
    phone BIGINT UNIQUE CHECK (phone >= 1000000000 AND phone <= 9999999999) ----CHECK & UNIQUE IS CONSTRAINTS
);

INSERT INTO passengers 
(name, age, gender, email, phone)
VALUES
('Ravi Kumar', 25, 'Male', 'ravikumar@gmail.com', 9876543210),
('Priya Sharma', 28, 'Female', 'priyasharma@gmail.com', 9123456780),
('Arjun Reddy', 32, 'Male', 'arjunreddy@gmail.com', 9988776655),
('Sneha Patel', 22, 'Female', 'snehapatel@gmail.com', 9090909090),
('Vikram Singh', 29, 'Other', 'vikramsingh@gmail.com', 9012345678);



--------------------
#bookingTable
----------------------
CREATE TABLE bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,              --PRIMARY KEY IS CONSTRAINT
    flight_id INT,
    passenger_id INT,
    booking_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    seat_no VARCHAR(10),
    total_fare FLOAT CHECK (total_fare > 0),                --CHECK IS CONSTRAINT
    status VARCHAR(15) CHECK (status IN ('Confirmed', 'Cancelled')),  --CHECK IS CONSTRAINT
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id) ON DELETE CASCADE,          --FOREIGN KEY IS CONSTRAINT
    FOREIGN KEY (passenger_id) REFERENCES passengers(passenger_id) ON DELETE CASCADE  --FOREIGN KEY IS CONSTRAINT
);

INSERT INTO bookings 
(flight_id, passenger_id, seat_no, total_fare, status)
VALUES
(1, 1, '12A', 3500.00, 'Confirmed'),
(2, 2, '07C', 4200.00, 'Confirmed'),
(3, 3, '18B', 3900.00, 'Cancelled'),
(4, 4, '10D', 4500.00, 'Confirmed'),
(5, 5, '05A', 2800.00, 'Confirmed');


--------------------
#pricingTable
----------------------
CREATE TABLE pricing (
    price_id INT AUTO_INCREMENT PRIMARY KEY,        --PRIMARY KEY IS CONSTRAINT
    flight_id INT,
    current_price FLOAT CHECK (current_price > 0),  --CHECK IS CONSTRAINT
    demand_factor FLOAT CHECK (demand_factor >= 0), --CHECK IS CONSTRAINT
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flight_id) REFERENCES flights(flight_id) ON DELETE CASCADE  --FOREIGN KEY IS CONSTRAINT
);

INSERT INTO pricing (flight_id, current_price, demand_factor)
VALUES
(1, 3850.00, 1.10),   -- IndiGo, 10% price increase
(2, 4410.00, 1.05),   -- Air India, 5% price increase
(3, 4290.00, 1.10),   -- SpiceJet, 10% increase
(4, 4725.00, 1.05),   -- Vistara, 5% increase
(5, 2660.00, 0.95);   -- Akasa Air, 5% discount (low demand)



--INSERT Queries
INSERT INTO passengers
(name,age,gender,email)
VALUES
('Neha',24,'Female','nehavarma@gmail.com');


INSERT INTO flights 
(airline_name, origin, destination, departure_time, arrival_time, total_seats, available_seats, base_price)
VALUES 
('GoAir', 'Delhi', 'Bangalore', '2025-10-15 07:00:00', '2025-10-15 09:30:00', 180, 175, 4000.00);


--UPDATE Queries
UPDATE flights
SET base_price=3000.00
WHERE flight_id=5;

UPDATE flights
SET available_seats=available_seats-1
WHERE flight_id=2;


UPDATE flights
SET base_price=base_price*1.10
WHERE available_seats <(total_seats*0.2);



--Delete Queries
DELETE from flights
WHERE flight_id =4;

DELETE from bookings
WHERE status='Cancelled';

--SELECT & WHERE Queries

SELECT * FROM flights

SELECT airline_name,base_price
FROM flights
WHERE base_price < 3000;

SELECT booking_id,flight_id,passenger_id,seat_no,total_fare
FROM bookings
WHERE status='Confirmed';

SELECT airline_name,origin, destination,departure_time,total_seats,available_seats,base_price
FROM flights
WHERE origin='Hyderabad';

--limit
SELECT airline_name,base_price
FROM flights
ORDER BY base_price ASC
LIMIT 2;

--ALTER
ALTER TABLE flights
ADD flight_no VARCHAR(20);


--JOIN Queries
SELECT p.name, p.email, b.booking_id, b.status
FROM passengers p
LEFT JOIN bookings b ON p.passenger_id = b.passenger_id;

SELECT f.airline_name, b.booking_id, b.status
FROM flights f
RIGHT JOIN bookings b ON f.flight_id = b.flight_id;

SELECT b.booking_id,p.name,f.airline_name,f.origin,f.destination,b.seat_no,b.total_fare,b.status
FROM bookings b 
INNER JOIN passengers p ON b.passenger_id=p.passenger_id
INNER JOIN flights f ON b.flight_id=f.flight_id;

SELECT f.flight_id, f.airline_name, b.booking_id, b.status
FROM flights f
LEFT JOIN bookings b ON f.flight_id = b.flight_id

UNION

SELECT f.flight_id, f.airline_name, b.booking_id, b.status
FROM flights f
RIGHT JOIN bookings b ON f.flight_id = b.flight_id;



--TRANSACTION
-- Start the transaction
START TRANSACTION;

-- 1. Check seat availability for flight_id = 1
SELECT available_seats 
FROM flights 
WHERE flight_id = 1;

-- 2. Update seat availability (reduce by 1)
UPDATE flights
SET available_seats = available_seats - 1
WHERE flight_id = 1
  AND available_seats > 0;

-- 3. Insert a new booking (if seats available)
INSERT INTO bookings (flight_id, passenger_id, seat_no, total_fare, status)
VALUES (1, 2, '14B', 3850.00, 'Confirmed');

-- 4. Commit the transaction
COMMIT;

-- 5. If any error occurs, rollback
ROLLBACK;



--CONSTRAINTS Verification
INSERT INTO passengers (name, age, gender, email)
VALUES ('Invalid Person', -5, 'Alien', 'invalid@gmail.com'); --will fail


--AGGREGATE & GROUP BY Queries

SELECT origin,base_price 
FROM flights
GROUP BY origin;

SELECT COUNT(*) AS total_flights 
FROM flights;

SELECT f.airline_name, f.flight_id, COUNT(b.booking_id) AS total_bookings
FROM flights f
JOIN bookings b ON f.flight_id = b.flight_id
GROUP BY f.airline_name, f.flight_id;


SELECT f.airline_name ,AVG(b.total_fare) AS avg_fare
FROM bookings b 
JOIN flights f ON b.flight_id=f.flight_id
GROUP BY f.airline_name;

