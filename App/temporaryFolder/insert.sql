USE digital_offices;

DELETE FROM users;

ALTER TABLE users AUTO_INCREMENT = 1;

INSERT INTO users(username, email, name, lastName, password, status, position, signature) VALUES("abiisnn", "abigail.nic.say@hotmail.com", "Abigail", "Nicolas", "123456789", "1", "Sistemas", "1234");
