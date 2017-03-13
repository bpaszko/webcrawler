from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import lxml
import polishstem
from datetime import datetime


class News():
	def __init__(self, title, desc, tp, subject, time, url):
		self.title = title
		self.desc = desc
		self.tp = tp
		self.subject = subject
		self.time = time
		self.url = url

	def __str__(self):
		return ("Title: " + self.title
		+ "\nDescription: " + self.desc
		+ "\nType: " + self.tp 
		+ "\nSubject: " + self.subject
 		+ "\nTime: " + self.time 
		+ "\nUrl: " + self.url )



def getBodyFromUrl(url):
	print(url)
	html = urlopen(url)
	bsObj = BeautifulSoup(html, "lxml")
	body = bsObj.body
	return body


def getNews(news):
	links = news.div.find_all("a")
	tp = links[1].string
	subject = links[-1].string
	time = news.find("div", class_="datePublished").stripped_strings
	time = next(time)
	data = news.find("a", title=True)
	url = data.get('href')
	title = data.get('title')
	description = data.find("div", class_=re.compile("hyphenate"))
	desc = next(description.stripped_strings)
	return News(title, desc, tp, subject, time, url)



def getDailyNews(body):
	global interesting
	news_list = []

	found = body.find_all("div", class_=re.compile("(itarticle)|(itshortvideo)"))
	for div in found:
		news = getNews(div)
		if not checkDate(news):
			return news_list
		if not checkSubject(news, interesting):
			continue	
		news_list.append(news)

	url = body.find('a', class_="nextPage").get('href')
	body = getBodyFromUrl("http://wiadomosci.onet.pl" + url)
	news_list += getDailyNews(body)
	return news_list
	


def checkDate(news):
	return not re.search('(dni)|(dzień)', news.time)




def checkSubject(news, interesting): 
	for word in interesting:
		pattern = re.compile(word)
		low_title = news.title.lower()
		low_desc = news.desc.lower()
		low_subj = news.subject.lower()
		if re.search(pattern, low_title) or re.search(pattern, low_desc) or re.search(pattern, low_subj):
			return True
	return False



interesting = []
with open("interesting.txt") as f:
	data = f.read()
	for line in data.split('\n'):
		if line:
			interesting.append(line.lower())


url = "http://wiadomosci.onet.pl/swiat"
body = getBodyFromUrl(url)

news_list = getDailyNews(body)


for news in news_list:
	print()
	print(news)







