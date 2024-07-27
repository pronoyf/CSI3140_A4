CREATE database HospitalTriage;
USE HospitalTriage;

CREATE TABLE Patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    name_ VARCHAR(255),
    code_ CHAR(3),
    severity_ ENUM('low', 'medium', 'high') NOT NULL,
    arrival_time INT
);


CREATE TABLE Admins(
	admin_id INT AUTO_INCREMENT PRIMARY KEY,
	username_ VARCHAR(255),
    password_ VARCHAR(255)
);

INSERT INTO Admins (username, password) VALUES ('admin', 'hashed_password_here');