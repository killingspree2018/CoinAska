INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`, `NoOfOrders`) VALUES ('Buy', '1', '0', '15', 'EqualVolumeDistribution', 20);
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`, `NoOfOrders`) VALUES ('Buy', '2', '15', '25', 'HighVolumeLowPrice', 20);
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `CustomEndPrice`, `BandAlgorithm`, `NoOfOrders`) VALUES ('Buy', '3', '25', '0.0027', 'GradualRestriction', 20);
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`, `NoOfOrders`) VALUES ('Sell', '1', '0', '15', 'EqualVolumeDistribution', 25);
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`, `NoOfOrders`) VALUES ('Sell', '2', '15', '25', 'HighVolumeLowPrice', 25);

INSERT INTO `coinaska`.`botconfigurables`(`ParameterName`, `Value`)
VALUES ('CustomBasePrice', NULL),
VALUES ('MovingAveragePeriod', 10);
