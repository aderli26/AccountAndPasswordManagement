DROP TABLE IF EXISTS `users`;
DROP TABLE IF EXISTS `login_retry`;
CREATE TABLE `users`(
  `username` VARCHAR(255) NOT NULL,
  `password` VARCHAR(255) NOT NULL);
CREATE TABLE `login_retry`(
  `username` VARCHAR(255) NOT NULL,
  `retry` INT NOT NULL,
  `timestamp` INT NOT NULL);