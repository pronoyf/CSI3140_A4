CREATE DATABASE hospital_db;

USE hospital_db;

-- Create Users Table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(10) NOT NULL,
    email VARCHAR(50) UNIQUE NOT NULL
);

-- Create Patients Table
CREATE TABLE patients (
    patient_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL,
    date_of_birth DATE,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- Create TriageStaff Table
CREATE TABLE triage_staff (
    staff_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    address VARCHAR(100) NOT NULL,
    role_desc VARCHAR(50) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (user_id)
);

-- Create Queue Table
CREATE TABLE queue (
    queue_id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    severity INT NOT NULL,
    wait_time INT NOT NULL,
    status VARCHAR(10) NOT NULL DEFAULT 'waiting',
    FOREIGN KEY (patient_id) REFERENCES patients (patient_id)
);
