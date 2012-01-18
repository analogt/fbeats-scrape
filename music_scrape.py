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
		else:
			del each
			continue
		for k,v in each['details'].iteritems():
			each[k] = v
		del each['details']
	print songs

def youtube(song):
	details = {}
	soup = bs(requests.get(song['url']).content)
	details['views'] = long(soup.findAll(
		'span',{"class":"watch-view-count"})[0].strong.string.replace(",",""))
	add_dt = soup.findAll('span',{"class":"watch-video-date"})[0].string
	add_dt = datetime.datetime.strptime(add_dt,'%b %d, %Y')
	today = datetime.datetime.today()
	days_old = (today - add_dt).days
	
	title = soup.findAll('span',{"id":"eow-title"})[0]['title']
	details['title'] = title
	details['vpd'] = details['views']/days_old
	return details

def soundcloud(song):
	details = {}

	soup = bs(requests.get(song['url']).content)
	try:
		details['views'] = long(soup.findAll('td',{"class":"total"})[0].string)
	except:
		details['views'] = None
	return details

if __name__ == '__main__':
	print "running"
	main()
