import praw
import csv
import html
from bs4 import BeautifulSoup

class Chapter(object):
	number = 0
	link = ""
	title = ""
	permalink = ""
	content = ""

	def __init__(self, n, l, t):
		self.number = n
		self.link = l
		self.title = t

chapterClass = "col-md-6 col-md-offset-3 col-sm-8 col-sm-offset-2 col-xs-10 col-xs-offset-1"
soup = BeautifulSoup(open('template.html', encoding="utf-8"), "html.parser")
main = soup.find(id="main")
reddit = "http://www.reddit.com/r/thephenomenon/comments/"
chapters = []
r = praw.Reddit(user_agent='phenomenon_aggregator.0.0.1')

output = open('index.html', 'w', encoding="utf-8")

with open('data.txt') as tsv:
	reader = csv.reader(tsv, delimiter='\t')
	lines = list(reader)
	for line in lines:
		chapters.append(Chapter(int(line[0]), str(line[1]).strip('/'), html.unescape(str(line[2]) )))

for chapter in chapters:
	container = soup.new_tag('div')
	container['class'] = chapterClass
	container['id'] = str(chapter.number)
	submissionLink = reddit + chapter.link
	if (chapter.link.count('/') == 2):
		submission = r.get_submission(submissionLink)
		content = submission.comments[0]
		chapter.permalink = content.permalink
		body = BeautifulSoup(content.body_html, "html.parser")
		if (chapter.title in body.contents[0].find('strong').text):
			body.contents[0].find('strong').parent.extract()
		if (body.contents[0].find('strong', string="EDIT:")):
			body.contents[0].find('strong', string="EDIT:").parent.extract()
		chapter.content = body
	else:
		split = chapter.link.split('/')
		submission = r.get_submission(submission_id=split[0])
		chapter.permalink = submission.permalink
		chapter.content = BeautifulSoup(submission.selftext_html, "html.parser")

	titleContainer = soup.new_tag('div')
	titleContainer['class'] = "titleContents"
	
	chapterNumber = soup.new_tag('h4')
	chapterNumber.append(str(chapter.number))
	titleContainer.append(chapterNumber)

	title = soup.new_tag('h2')
	title.append(chapter.title)
	titleContainer.append(title)

	alink = soup.new_tag('a')
	alink['href'] = chapter.permalink
	alink['class'] = "permalink"
	link = soup.new_tag('h3')
	icon = soup.new_tag('small')
	icon['class'] = "glyphicon glyphicon-link"
	link.append(icon)
	alink.append(link)
	titleContainer.append(alink)

	container.append(titleContainer)
	container.append(chapter.content)	
	main.append(container)
	print (chapter.number)

print (soup, file=output)