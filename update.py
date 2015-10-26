import praw
import html
import re
import time
import datetime
from html import parser
from bs4 import BeautifulSoup
from praw import helpers

"""https://github.com/voussoir/reddit/blob/master/Prawtimestamps/timesearch.py"""
MAXIMUM_EXPANSION_MULTIPLIER = 2

def human(timestamp):
	x = datetime.datetime.utcfromtimestamp(timestamp)
	x = datetime.datetime.strftime(x, "%b %d %Y %H:%M:%S")
	return x

def humannow():
	x = datetime.datetime.now(datetime.timezone.utc).timestamp()
	x = human(x)
	return x

def get_all_posts(r, subreddit, titleText, lower):
	'''
	Get submissions from a subreddit or user between two points in time
	'''
	
	interval=86400*128
	offset = -time.timezone
	lower -= offset
	maxupper = datetime.datetime.now(datetime.timezone.utc).timestamp()
	usermode = 'Emperor_Cartagia'
	lower -= offset
	maxupper -= offset
	cutlower = lower
	cutupper = maxupper
	upper = lower + interval
	subreddit = subreddit.display_name

	allResults = []
	
	toomany_inarow = 0
	while lower < maxupper:
		print('\nCurrent interval:', interval, 'seconds')
		print('Lower', human(lower), lower)
		print('Upper', human(upper), upper)
		while True:
			try:
				query = '(and author:\'%s\' timestamp:%d..%d title:\'%s\')' % (usermode, lower, upper, titleText)
				searchresults = list(r.search(query, subreddit=subreddit,
											  sort='new', limit=100,
											  syntax='cloudsearch'))
				break
			except:
				traceback.print_exc()
				print('resuming in 5...')
				time.sleep(5)
				continue

		searchresults.reverse()
		allResults += searchresults			

		itemsfound = len(searchresults)
		print('Found', itemsfound, 'items')
		if itemsfound < 75:
			print('Too few results, increasing interval', end='')
			diff = (1 - (itemsfound / 75)) + 1
			diff = min(MAXIMUM_EXPANSION_MULTIPLIER, diff)
			interval = int(interval * diff)
		if itemsfound > 99:
			#Intentionally not elif
			print('Too many results, reducing interval', end='')
			interval = int(interval * (0.8 - (0.05*toomany_inarow)))
			upper = lower + interval
			toomany_inarow += 1
		else:
			lower = upper
			upper = lower + interval
			toomany_inarow = max(0, toomany_inarow-1)

	print()
	return allResults

class Chapter(object):
	number = 0
	link = ""
	title = ""
	permalink = ""
	content = ""
	soupContainer = None

	def __init__(self, n, l, t):
		self.number = n
		self.link = l
		self.title = t

	def GetSoupChapter(self):
		self.soupContainer = soup.new_tag('div')
		self.soupContainer['class'] = chapterClass
		self.soupContainer['id'] = str(self.number)
		titleContainer = soup.new_tag('div')
		titleContainer['class'] = "titleContents"

		chapterNumber = soup.new_tag('h4')
		chapterNumber.append(str(self.number))
		titleContainer.append(chapterNumber)

		title = soup.new_tag('h2')
		title.append(self.title)
		titleContainer.append(title)

		alink = soup.new_tag('a')
		alink['href'] = self.permalink
		alink['class'] = "permalink"
		link = soup.new_tag('h3')
		icon = soup.new_tag('small')
		icon['class'] = "glyphicon glyphicon-link"
		link.append(icon)
		alink.append(link)
		titleContainer.append(alink)

		self.soupContainer.append(titleContainer)
		self.soupContainer.append(self.content)

chapterClass = "col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-10 col-xs-offset-1"
index = open('index.html', 'r', encoding="utf-8")
soup = BeautifulSoup(index, "html.parser")
index.close()
main = soup.find(id="main")
lastLink = main.contents[-1].find('a')['href']

reddit = "http://www.reddit.com/r/thephenomenon/comments/"
chapters = []
r = praw.Reddit(user_agent='phenomenon_aggregator.0.0.1')
subreddit = r.get_subreddit("ThePhenomenon")   

lastSubmission = r.get_submission(lastLink)
allSubmissions = get_all_posts(r, subreddit, "Chapter", lastSubmission.created_utc)
index = open('index.html', 'w', encoding="utf-8")

for submission in allSubmissions:
	if (not ':' in submission.title or 'discussion' in submission.title.lower()):
		continue
	titleSplit = submission.title.split(':')
	number = titleSplit[0].split(' ')[1]
	title = titleSplit[1].strip(' ')
	chapter = Chapter(int(number), "", html.unescape(title))
	chapter.permalink = submission.permalink
	chapter.content = BeautifulSoup(submission.selftext_html, "html.parser")
	chapter.GetSoupChapter()
	chapters.append(chapter)

chapters.sort(key=lambda c: c.number)

for chapter in chapters:
	print (chapter.number)	
	main.append(chapter.soupContainer)

print (soup, file=index)
index.close()