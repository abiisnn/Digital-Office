DROP database digital_office;
create database digital_office;
USE digital_office;

DELETE FROM users;

ALTER TABLE users AUTO_INCREMENT = 1;

INSERT INTO users(username, email, name, lastName, password, status, position, signature) VALUES("abiisnn", "abigail.nic.say@hotmail.com", "Abigail", "Nicolas", "123456789", "1", "Sistemas", "1234");
UPDATE meeting SET issue='Firma de abogados' WHERE idMeeting=1;

UPDATE meeting SET date='May 22, 2019' WHERE idMeeting=1;

UPDATE users SET position='CEO' WHERE idPerson=1;

UPDATE users SET position='RH' WHERE idPerson=6;