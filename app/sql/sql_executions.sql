CREATE TABLE MASTER_EMPLOYEES (
    employee_id INT,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    hire_date DATE,
    end_date DATE,
    user_password VARCHAR(255),
    role VARCHAR(50),
    PRIMARY KEY (employee_id)
);


CREATE TABLE access_employees (
    access_id INT NOT NULL AUTO_INCREMENT,
    employee_id INT NOT NULL,
    access_time DATETIME NOT NULL,
    creator_username VARCHAR(50),
    PRIMARY KEY (access_id),
    FOREIGN KEY (employee_id) REFERENCES MASTER_EMPLOYEES(employee_id)
);

--Population

INSERT INTO venue.MASTER_EMPLOYEES (employee_id, first_name, last_name, email, hire_date, end_date, user_password, role) VALUES
(1, 'John', 'Doe', 'john.doe@example.com', '2021-03-15', NULL, 'jd2021!', 'Manager'),
(2, 'Jane', 'Smith', 'jane.smith@example.com', '2019-06-20', NULL, 'js2019!', 'Developer'),
(3, 'Alice', 'Johnson', 'alice.johnson@example.com', '2020-07-30', NULL, 'aj2020!', 'Analyst'),
(4, 'Bob', 'White', 'bob.white@example.com', '2022-01-12', NULL, 'bw2022!', 'Support'),
(5, 'Charlie', 'Brown', 'charlie.brown@example.com', '2018-11-25', NULL, 'cb2018!', 'Designer'),
(6, 'David', 'Green', 'david.green@example.com', '2023-02-17', NULL, 'dg2023!', 'Sales'),
(7, 'Ella', 'Black', 'ella.black@example.com', '2021-08-05', '2024-03-10', 'eb2021!', 'HR'),
(8, 'Frank', 'Gray', 'frank.gray@example.com', '2019-12-15', NULL, 'fg2019!', 'Marketing'),
(9, 'Grace', 'Adams', 'grace.adams@example.com', '2020-09-04', NULL, 'ga2020!', 'Finance'),
(10, 'Henry', 'Wells', 'henry.wells@example.com', '2018-05-20', NULL, 'hw2018!', 'CEO');

INSERT INTO venue.access_employees (employee_id, access_time, creator_username) VALUES
(1, '2024-04-17 08:30:00', 'admin'),
(3, '2024-04-17 08:30:00', 'admin'),
(2, '2024-04-17 08:30:00', 'admin'),
(4, '2024-04-17 08:30:00', 'admin'),
(5, '2024-04-17 08:30:00', 'admin'),
(9, '2024-04-17 08:30:00', 'admin'),
(4, '2024-04-17 08:30:00', 'admin'),
(6, '2024-04-17 08:30:00', 'admin'),
(8, '2024-04-17 08:30:00', 'admin'),
(5, '2024-04-17 08:30:00', 'admin'),
(7, '2024-04-17 08:30:00', 'admin'),
(9, '2024-04-17 08:30:00', 'admin'),
(10, '2024-04-17 08:30:00', 'admin'),
(2, '2019-07-15 09:00:00', 'admin'),
(3, '2020-08-10 10:30:00', 'admin'),
(4, '2022-01-18 11:00:00', 'admin'),
(5, '2019-01-05 12:15:00', 'admin'),
(6, '2023-03-15 13:45:00', 'admin'),
(7, '2021-08-10 14:30:00', 'admin'),
(8, '2020-01-12 15:00:00', 'admin'),
(9, '2020-10-03 16:45:00', 'admin'),
(10, '2018-06-30 17:30:00', 'admin');


UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$rvGa8EqZ288chhKqHH3JfOqJ1/ENyYCXEn1vMe9PUZUu2idskseU6' WHERE employee_id = 1;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$VwQuEQVkBvZ/6UuyoCDGYOSqmHQz2SHpJ9CYSV/7luFE00xg2JxLi' WHERE employee_id = 2;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$3C5m1Y2ro0GrRCCi6oZLyO3Z.UWytCP7ENj0uA3eOnOuoxV.YRRyu' WHERE employee_id = 3;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$C8H3bbSG9NdggnkyUkvEWeOgaAhAJIb5DPYEz1FE3TbaTWyprhnkG' WHERE employee_id = 4;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$ecnD9xuLalIuZW6keiXQu.KHk1wcHqJ.nDprcseRsJwwVrplM8QzO' WHERE employee_id = 5;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$vWw9.DOI4dCOHM0QoEUuMOSBLAEJGdZ3aH8zFXoA21wSo/Rxbdj2G' WHERE employee_id = 6;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$0SM.aZvVhHoJOgg.VY8ulOrfJgJgyXxV2fccnY969xjKfZaGRtmOW' WHERE employee_id = 7;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$hbTdBr52cPUp3liyNcFsKe482.Q9QIRb9PlKYPOt5aLbtHHfLO/Ay' WHERE employee_id = 8;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$MySJR9LApAkxj6s4lMXVN.t0KsofDxOTUEvhFga1sl8yMWG2vlXX.' WHERE employee_id = 9;
UPDATE  venue.MASTER_EMPLOYEES SET user_password = '$2b$12$OCAlxQfCZkzTKe2lgFeBN.qr39gcfjIgvMoeJnFVCoACiggdI3UsO' WHERE employee_id = 10;
