INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`) VALUES ('Buy', '1', '0', '15', 'EqualVolumeDistribution');
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`) VALUES ('Buy', '2', '15', '25', 'HighVolumeLowPrice');
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `CustomEndPrice`, `BandAlgorithm`) VALUES ('Buy', '3', '25', '0.0027', 'GradualRestriction');
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`) VALUES ('Sell', '1', '0', '15', 'EqualVolumeDistribution');
INSERT INTO `coinaska`.`pricebands` (`Type`, `BandName`, `StartPercentage`, `EndPercentage`, `BandAlgorithm`) VALUES ('Sell', '2', '15', '25', 'HighVolumeLowPrice');

INSERT INTO `coinaska`.`botconfigurables`(`ParameterName`, `Value`)
VALUES ('CustomBasePrice', NULL),
VALUES ('MovingAveragePeriod', 10),
VALUES ('AccountBalance', NULL);
