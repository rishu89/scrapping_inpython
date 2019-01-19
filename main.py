import requests
import json
from bs4 import BeautifulSoup
import os, os.path, csv
import mysql.connector
#SET @@global.sql_mode= 'NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';
mydb=mysql.connector.connect(
	host="localhost",
	user="root",
	passwd="123_password"
	)
print(mydb)
mycursor=mydb.cursor()
mycursor.execute("USE details")
#mycursor.execute("CREATE TABLE detail (title VARCHAR(255),subtitle VARCHAR(255),image_url VARCHAR(255),claps VARCHAR(255),author VARCHAR(255),post_creation VARCHAR(255),reading_time VARCHAR(255))")
title=[]
subtitle=[]
image_url=[]
reading_time=[]
author=[]
post_creation=[]
claps=[]
with open("input.txt") as f:
	for line in f.readlines():
		line = line.rstrip("\n")
		print(line)
		res = requests.get(line)
		soup = BeautifulSoup(res.text,"html.parser")
		for i in soup.select('title'):
			title.append(i.text)
			print(i.text)
		for i in soup.select('h4'):
			subtitle.append(i.text)
			print(i.text)
		i=soup.select('.js-multirecommendCountButton')
		claps.append(i[0].text)
		print(i[0].text)
		for i in soup.select('.avatar-image'):
			image_url.append(i['src'])
			print(i['src'])
		for read in soup.select('.readingTime'):
			reading_time.append(read['title'])
			print(read['title'])
		date=soup.select('.ui-caption')
		post_creation.append(date[0].text)
		print(date[0].text)
		author=soup.find_all(True,{"class":["link--darker","postMetaInline--author"]})
		author.append(author[0].text)
		print(author[0].text)
		print('\n')
print(title)
query1="INSERT INTO detail (title,subtitle,image_url,claps,author,post_creation,reading_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
mycursor.execute(query1,(str(title),str(subtitle),str(image_url),str(claps),str(author),str(post_creation),str(reading_time)))
mydb.commit()