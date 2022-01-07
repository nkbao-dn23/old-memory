CREATE DATABASE bank;
USE bank;

CREATE TABLE `profile` (
  `Id` varchar(100) NOT NULL,
  `Password` varchar(100) NOT NULL,
  `Username` varchar(100) NOT NULL,
  `Money` varchar(100) NOT NULL
  
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


INSERT INTO `profile` (`Id`, `Password`, `Username`, `Money`) VALUES
('hades1', 'CuT', 'Tran Duc Bo', '1333337'),
('hades2', 'CuT', 'Hot girl Q_Cam', '100'),
('hades3', 'CuT', 'Co be quang khan tam', '100'),
('hades4', 'CuT', 'Tram Anh', '100'),
('hades5', 'CuT', 'Hotgirl bella', '998'),
('hades6', 'CuT', 'Happy Polla', '999'),
('hades7', 'CuT', 'Hades', '100000');
COMMIT;



CREATE USER 'vietnam' IDENTIFIED BY 'asddva8439hefe4j';
GRANT SELECT ON bank.* to 'vietnam'@'%';
FLUSH PRIVILEGES;
