import requests
from BeautifulSoup import BeautifulSoup as bs
import datetime
import re

def main():
	songs = reddit()

def reddit():
	songs = []
	
	soup = bs(requests.get('http://reddit.com/r/futurebeats').content)
	soup = soup.findAll('p',{"class":"title"})
	
	for each in soup:
		songs.append({"title": each.a.string , "url": each.a['href']})

	yt = r".youtube.com+"
	sc = r".soundcloud\.com+"
	pattern = re.compile(r'(.youtube.com)')
	for each in songs:
		if re.search(yt,each['url']):
			each['details'] = youtube(each)
		elif re.search(sc,each['url']):
			each['details'] = soundcloud(each)
	print songs

def youtube(song):
	soup = bs(requests.get(song['url']).content)
	views = long(soup.findAll('span',{"class":"watch-view-count"})[0].strong.string.replace(",",""))
	add_dt = soup.findAll('span',{"class":"watch-video-date"})[0].string
	add_dt = datetime.datetime.strptime(add_dt,'%b %d, %Y')
	title = soup.findAll('span',{"id":"eow-title"})[0]['title']

	print views, add_dt, title, song['url']
def soundcloud(song):
	pass

if __name__ == '__main__':
	print "running"
	main()
