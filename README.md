# Web Crawler

It crawls data from websites and insert into database.

Required:
1. Python 3.9.1 (pip install mysql-connector-python requests bs4 lxml)
1. XAMPP 8.0.2
1. DBeaver-ce-7.3.5


Create Table:
CREATE TABLE `stock_price` (
  `Stock` varchar(100) NOT NULL,
  `Price` float DEFAULT NULL,
  `Volume` int(11) DEFAULT NULL,
  `Updated` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
