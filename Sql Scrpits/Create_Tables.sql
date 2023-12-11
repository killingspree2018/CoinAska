CREATE DATABASE `coinaska`
CREATE TABLE `coinaska`.`pricebands` (
  `ID` INT NOT NULL AUTO_INCREMENT,
  `Type` VARCHAR(45) NULL,
  `BandName` VARCHAR(45) NULL,
  `StartPercentage` FLOAT NULL,
  `EndPercentage` FLOAT NULL,
  `CustomEndPrice` FLOAT NULL,
  `PriceDifferenceRangeStart` FLOAT NULL,
  `PriceDifferenceRangeEnd` FLOAT NULL,
  `BandAlgorithm` VARCHAR(45) NULL,
  `AccountBalancePercentage` INT NULL,
  `CustomAccountBalance` FLOAT NULL;
  `NoOfOrders` INT NULL;
  PRIMARY KEY (`ID`),
  UNIQUE INDEX `ID_UNIQUE` (`ID` ASC) VISIBLE
);

CREATE TABLE `coinaska`.`botconfigurables` (
  `ParameterName` varchar(45) NOT NULL,
  `Value` float DEFAULT NULL,
  PRIMARY KEY (`ParameterName`),
  UNIQUE KEY `ParameterName_UNIQUE` (`ParameterName`)
);

CREATE TABLE `coinaska`.`coinpricetracker` (
  `Price` float NOT NULL,
  `CurrentTime` DATETIME NULL,
  PRIMARY KEY (`CurrentTime`)
);

