-- Create the database
CREATE DATABASE IF NOT EXISTS railway;
USE railway;

-- Create train_info table
CREATE TABLE IF NOT EXISTS train_info (
    Train_No VARCHAR(10) NOT NULL,
    Station_Code VARCHAR(20) NOT NULL,
    Station_Name VARCHAR(30) NOT NULL,
    Arrival_Time VARCHAR(20) NOT NULL,
    Departure_Time VARCHAR(20) NOT NULL,
    Distance VARCHAR(10) NOT NULL,
    Source_Station_Code VARCHAR(20) NOT NULL,
    Source_Station_Name VARCHAR(70) NOT NULL,
    Destination_Station_Code VARCHAR(20) NOT NULL,
    Destination_Station_Name VARCHAR(60) NOT NULL
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    Train_No INT NOT NULL,
    Passenger_Name VARCHAR(30) NOT NULL,
    Mobile_No VARCHAR(10) NOT NULL,
    Passenger_Adhaar VARCHAR(12) NOT NULL,
    Time_Of_Booking DATETIME NOT NULL,
    Booking_ID INT PRIMARY KEY,
    Class VARCHAR(20) NOT NULL
);

-- Insert sample train data
INSERT INTO train_info (Train_No, Station_Code, Station_Name, Arrival_Time, Departure_Time, Distance, Source_Station_Code, Source_Station_Name, Destination_Station_Code, Destination_Station_Name) VALUES
('12345', 'DLI', 'Delhi Junction', '08:00:00', '08:15:00', '0', 'DLI', 'Delhi Junction', 'BCT', 'Mumbai Central'),
('12345', 'AGC', 'Agra Cantt', '10:30:00', '10:35:00', '200', 'DLI', 'Delhi Junction', 'BCT', 'Mumbai Central'),
('12345', 'BCT', 'Mumbai Central', '20:00:00', '20:00:00', '1400', 'DLI', 'Delhi Junction', 'BCT', 'Mumbai Central'),
('67890', 'BCT', 'Mumbai Central', '09:00:00', '09:15:00', '0', 'BCT', 'Mumbai Central', 'DLI', 'Delhi Junction'),
('67890', 'JHS', 'Jhansi Junction', '15:45:00', '15:50:00', '800', 'BCT', 'Mumbai Central', 'DLI', 'Delhi Junction'),
('67890', 'DLI', 'Delhi Junction', '22:30:00', '22:30:00', '1400', 'BCT', 'Mumbai Central', 'DLI', 'Delhi Junction'),
('54321', 'MAS', 'Chennai Central', '07:30:00', '07:45:00', '0', 'MAS', 'Chennai Central', 'SBC', 'Bangalore City'),
('54321', 'KPD', 'Katpadi Junction', '10:15:00', '10:20:00', '130', 'MAS', 'Chennai Central', 'SBC', 'Bangalore City'),
('54321', 'SBC', 'Bangalore City', '13:00:00', '13:00:00', '360', 'MAS', 'Chennai Central', 'SBC', 'Bangalore City');

-- Insert sample booking data
INSERT INTO bookings (Train_No, Passenger_Name, Mobile_No, Passenger_Adhaar, Time_Of_Booking, Booking_ID, Class) VALUES
(12345, 'Raj Sharma', '9876543210', '123456789012', NOW(), 1001, 'AC-2'),
(67890, 'Priya Patel', '8765432109', '234567890123', NOW(), 1002, 'Sleeper'),
(54321, 'Amit Singh', '7654321098', '345678901234', NOW(), 1003, 'AC-3'),
(12345, 'Sneha Verma', '6543210987', '456789012345', NOW(), 1004, 'AC-1');

-- Create indexes for faster queries
CREATE INDEX idx_source_dest ON train_info (Source_Station_Code, Destination_Station_Code);
CREATE INDEX idx_mobile ON bookings (Mobile_No);
CREATE INDEX idx_booking_id ON bookings (Booking_ID);

-- Create a view for station codes
CREATE VIEW station_codes AS
SELECT DISTINCT 
    Source_Station_Code AS station_code, 
    Source_Station_Name AS station_name 
FROM train_info
UNION
SELECT DISTINCT 
    Destination_Station_Code AS station_code, 
    Destination_Station_Name AS station_name 
FROM train_info;