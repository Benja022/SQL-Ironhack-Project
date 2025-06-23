CREATE DATABASE IF NOT EXISTS gymSQL;
USE gymSQL;

-- Changing type text to datetime in columns checkin, checkout
ALTER TABLE `gymSQL`.`checkin_checkout_history_updated` 
CHANGE COLUMN `checkin_time` `checkin_time` DATETIME NULL DEFAULT NULL ,
CHANGE COLUMN `checkout_time` `checkout_time` DATETIME NULL DEFAULT NULL ;

UPDATE checkin_checkout_history_updated 
SET checkin_time = STR_TO_DATE(checkin_time, '%Y-%m-%d %H:%i:%s'),
    checkout_time = STR_TO_DATE(checkout_time, '%Y-%m-%d %H:%i:%s');