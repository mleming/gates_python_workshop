#See https://docs.python.org/2/library/re.html for regex references

import urllib2
import re

# PART 1 - Regex the URLs out of a webpage
# Prints out all URLs in the webpage
# First, simpler part of program
url = "http://google.com/"
data = urllib2.urlopen(url)
webpage = data.read()
m = re.findall('https?:\/\/[^\/]*',webpage)
for address in m:
	print address

# PART 2 - Stick it in a method
# Put it all into a method. This method returns an array of all URLs in a
# webpage

def pyscrape(url):
	try:
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		data = urllib2.urlopen( req )
		webpage = data.read()
	except:
		# If opening the URL doesn't work for some reason
		print "Error: " + url
		return []
	return re.findall('https?:\/\/[\.a-zA-Z]*\/',webpage)

# PART 3 - Recursion
def pyscrape_recurse(url, depth = 0):
	try:
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
		data = urllib2.urlopen( req )
		webpage = data.read()
	except:
		# If opening the URL doesn't work for some reason
		print "Error: " + url
		return []
	urls_in_webpage = re.findall('https?:\/\/[\.a-zA-Z]*\/',webpage)
	if depth == 5:
		return urls_in_webpage
	for urls in urls_in_webpage:
		urls_in_webpage = urls_in_webpage + pyscrape_recurse(depth + 1)
	return urls_in_webpage

# PART 4 - BFS and DFS and other fancy regex stuff.
# This program uses a search to keep following links on webpages. It does more
# complicated things, like not following links to previously-visited websites,
# which means that this whole thing will definitely fill up two hours.
def printscrape(breadth, top_url):
	# If breadth == True, this performs a breadth-first search.
	# If breadth == False, this performs a depth-first search.
	pop_end = -1 if breadth else 0
	stack = []
	stack.append(top_url)
	frontier = []
	i = 0
	while len(stack) > 0:
		i += 1
		if i == 100: # Stops it from running forever.
			print frontier
			return
		foo = stack[pop_end]
		print stack[pop_end]
		del stack[pop_end]
		for d in pyscrape(foo):
			try:
			# This regular expression will match the ".google.com/"
			# in "https://www.google.com/". It's used in this context to
			# make sure that we're calling a unique website each time instead of
			# different parts of the same website (so, if we access
			# "https://www.google.com/", the search will ignore
			# "https://news.google.com/"
				mm = re.search('[a-zA-Z]+\.[a-zA-Z]+\/$',d).group(0)
				if not(any(mm in f for f in frontier)):
					frontier.append(d)
					stack.append(d)
			except:
				print d

printscrape(True,"https://google.com/")
