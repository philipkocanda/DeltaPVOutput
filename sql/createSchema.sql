CREATE DATABASE deltapv;

CREATE TABLE Measurement(
  id INT key auto_increment,
  inverterId int,
  tsmp TIMESTAMP,
  dcVoltage int,
  dcPower int,
  acPower int
) ENGINE = INNODB;
