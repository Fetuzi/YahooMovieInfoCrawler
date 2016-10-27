#!/usr/bin/python
# -*- coding: UTF-8 -*-
#encoding=utf-8
from scrapy.selector import Selector
from scrapy.http import HtmlResponse
import urllib2
import MySQLdb
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class MovieTimeDBModifier:
  def __init__(self, host, user, password, database):
    self.conn = MySQLdb.connect( host     = host,
                                 user     = user,
                                 passwd   = password,
                                 db       = database,
                                 charset  = 'utf8')
    self.cursor =  self.conn.cursor()
  
  def CreateTable(self, table):
    query = 'CREATE TABLE MovieTime (Movie VARCHAR(255) CHARACTER SET utf8, \
    Area LONGTEXT CHARACTER SET utf8, \
    Theater VARCHAR(255) CHARACTER SET utf8,  \
    PhoneNumber VARCHAR(255) CHARACTER SET utf8,  \
    Time VARCHAR(255) CHARACTER SET utf8  \
    );'
    self.cursor.execute(query)

  def RemoveTable(self, table):
    query = "DROP TABLE " + table
    self.cursor.execute(query)

  def InsertToDatabase(self, table, movieId, area, theater, theaterNumber, time):
    query = "INSERT INTO "+ table + " VALUES (%s, %s, %s, %s, %s)"
    self.cursor.execute(query ,(movieId, area, theater, theaterNumber, time))
    self.conn.commit()

  def mysqlconnect(self):
    query = "SELECT * FROM " + self.table
    self.cursor.execute (query)
    row = self.cursor.fetchone()
    print "server version:", row[0]
  
  def disconnection(self): 
    self.cursor.close ()
    self.conn.close ()

def CrawlMovieTime(id, area):
  url = 'https://tw.movies.yahoo.com/movietime_result.html?id='+str(id)+'&area='+str(area)
  body = urllib2.urlopen(url).read()
  crawled_movieTime = Selector(text=body, type='html').xpath('//div[@class="mtcontainer clearfix"]//text()').extract()
  crawled_movieTheater = Selector(text=body, type='html').xpath('//div[@class="img"]//a//text()').extract()
  crawled_movieTheater_number = Selector(text=body, type='html').xpath('//div[@class="img"]//p//text()').extract()
  return crawled_movieTime, crawled_movieTheater, crawled_movieTheater_number

def get_Areas():
  Areas = {}; 
  Areas[6] = '台北'; Areas[8] = '新北'; Areas[3] = '台北二輪'; Areas[18] = '基隆'; Areas[16] = '桃園'; Areas[1] = '中壢'
  Areas[20] = '新竹'; Areas[15] = '苗栗'; Areas[2] = '台中'; Areas[22] = '彰化'; Areas[19] = '雲林'; Areas[13] = '南投'
  Areas[21] = '嘉義'; Areas[10] = '台南'; Areas[17] = '高雄'; Areas[11] = '宜蘭'; Areas[12] = '花蓮'; Areas[9] = '台東'
  Areas[14] = '屏東'; Areas[24] = '金門'
  return Areas

def get_movies():
  url = 'https://tw.movies.yahoo.com/movie_intheaters.html?p=1'
  body = urllib2.urlopen(url).read()
  tmp1 = Selector(text=body, type='html').xpath('//div[@id="hd"]//select[@name="id"]//option/@value').extract()
  tmp2 = Selector(text=body, type='html').xpath('//div[@id="hd"]//select[@name="id"]//option/text()').extract()
  return dict(zip(tmp1[1:len(tmp1)], tmp2[1:len(tmp2)]))

def main():
  movies = get_movies()
  areas = get_Areas()
  DBModifier = MovieTimeDBModifier( host      = "localhost",
                                    user      = "root",
                                    password  = "yihming0716",
                                    database  = "fuck")
  try:
    DBModifier.RemoveTable('MovieTime')
    DBModifier.CreateTable('MovieTime')
  except:
    DBModifier.CreateTable('MovieTime')

  for movieId in movies:
    #print movieId
    print 'crawling ' + str(movies[movieId]) + ' . . . '
    for area in areas:
      #print 'crawling ' + str(movies[movieId]) + ' '  + str(areas[area])
      crawled_movieTimes, crawled_movieTheater, crawled_movieTheater_number = CrawlMovieTime(movieId, area)

      k = -1
      for time in crawled_movieTimes:
        if time == ' ' or time == ' | ':
          pass
        elif time == '\n':
          k = k + 1
        else:
          
          try:
            DBModifier.InsertToDatabase('MovieTime', movies[movieId], areas[area]
              , crawled_movieTheater[k], crawled_movieTheater_number[k], time) 
          except:
            DBModifier.InsertToDatabase('MovieTime', movies[movieId], areas[area]
              , crawled_movieTheater[k], 'None', time)   

  DBModifier.disconnection()

if __name__ == '__main__':
  main()


