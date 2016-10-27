# About
抓取yahoo上映電影、區域、電影院、影城電話與電影時刻,並且存入MySQL。

# Library
- Scrapy
- urllib2
- MySQLdb

# Usage
#### 設定資料庫連線
host, user, password, database在75~78行。
#### 運行
$ python yahoo_MovieInfo_crawler.py

# Database
- Movie
- Area
- Theater
- PhoneNumber
- ShowTimes
