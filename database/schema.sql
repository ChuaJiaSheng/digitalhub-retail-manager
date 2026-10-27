-- Structure derived from the original DigitalHub coursework database.
-- No original row data, password hashes or peppers are included.
CREATE DATABASE IF NOT EXISTS digitalhub;
USE digitalhub;
SET FOREIGN_KEY_CHECKS=0;

CREATE TABLE `customers` (
  `Customers_ID` int NOT NULL AUTO_INCREMENT,
  `Customers_Name` varchar(45) DEFAULT NULL,
  `Customers_Gender` varchar(45) DEFAULT NULL,
  `Customers_City` varchar(45) DEFAULT NULL,
  `Customers_State_Code` varchar(45) DEFAULT NULL,
  `Customers_State` varchar(45) DEFAULT NULL,
  `Customers_Zip_Code` varchar(45) DEFAULT NULL,
  `Customers_Country` varchar(45) DEFAULT NULL,
  `Customers_Continent` varchar(45) DEFAULT NULL,
  `Customers_Birthday` date DEFAULT NULL,
  PRIMARY KEY (`Customers_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `order_details` (
  `Order_Details_ID` int NOT NULL AUTO_INCREMENT,
  `Order_Number` int DEFAULT NULL,
  `Line_Item` int DEFAULT NULL,
  `Purchased_Quantity` int DEFAULT NULL,
  PRIMARY KEY (`Order_Details_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `orders` (
  `Orders_ID` int NOT NULL AUTO_INCREMENT,
  `Order_Details_ID` int DEFAULT NULL,
  `Order_Date` date DEFAULT NULL,
  `Delivery_Date` date DEFAULT NULL,
  `Customers_ID` int DEFAULT NULL,
  `Stores_ID` int DEFAULT NULL,
  `Product_ID` int DEFAULT NULL,
  PRIMARY KEY (`Orders_ID`),
  KEY `FKStoreID_idx` (`Stores_ID`),
  KEY `FKOrderNumber_idx` (`Order_Details_ID`),
  KEY `FKCustomerID_idx` (`Customers_ID`),
  KEY `FKProductID_idx` (`Product_ID`),
  CONSTRAINT `FKCustomerID` FOREIGN KEY (`Customers_ID`) REFERENCES `customers` (`Customers_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FKOrderDetailsID` FOREIGN KEY (`Order_Details_ID`) REFERENCES `order_details` (`Order_Details_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FKProductID` FOREIGN KEY (`Product_ID`) REFERENCES `products` (`Products_ID`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `FKStoresD` FOREIGN KEY (`Stores_ID`) REFERENCES `stores` (`Stores_ID`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `products` (
  `Products_ID` int NOT NULL AUTO_INCREMENT,
  `Product_Name` varchar(100) DEFAULT NULL,
  `Product_Brand` varchar(100) DEFAULT NULL,
  `Product_Color` varchar(45) DEFAULT NULL,
  `Product_Unit_Cost` decimal(10,2) DEFAULT NULL,
  `Product_Unit_Price` decimal(10,2) DEFAULT NULL,
  `Product_Category` varchar(100) DEFAULT NULL,
  `Product_Subcategory` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`Products_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `stores` (
  `Stores_ID` int NOT NULL AUTO_INCREMENT,
  `Stores_Country` varchar(45) DEFAULT NULL,
  `Stores_State` varchar(45) DEFAULT NULL,
  `Stores_Square_Meters` int DEFAULT NULL,
  `Stores_Open_Date` date DEFAULT NULL,
  PRIMARY KEY (`Stores_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(100) NOT NULL,
  `hashed_password` varchar(255) NOT NULL,
  `pepper` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username_UNIQUE` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

SET FOREIGN_KEY_CHECKS=1;
