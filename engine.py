# graph={url1:[outlink1,outlink2], url1:[outlink3, outlink4]}
# ranks={url1:1/N, url2: 1/N, }

def compute_ranks ( graph ):
  d = 0.8 # damping factor
  N = len ( graph ) # number of pages
  numloops = 10 # effects the accuracy
  ranks = {}
  #initialize the rankings of each url
  for page in graph :
    ranks [page] = 1/ N

  for i in range (0 , numloops) :
    newranks = {}
    for page in graph:
      newrank = (1 - d ) / N
      for node in graph :
        if page in graph [node]:
          newrank = newrank + d *(ranks[node]/len(graph[node]))
      newranks [page] = newrank
    ranks = newranks
  return newranks

def lookup(keyword, index):
  for element in index:
    if element == keyword:
      return index[element]
    else:
      None

def lookup_sorted(keyword, index ,rankIndex) :
  for element in index:
    if element == keyword:
      return sorted(index[keyword] , key = rankIndex.get , reverse = True)
    else:
      None

def add_to_index(keyword,index,url):
  if lookup(keyword, index) == None:
    index[keyword] = [url]
    return index
  for element in index:
    if element == keyword:
      if url not in index[element]:
        index[element].append(url)
        return index
  return index

def add_page_to_index(index, url):
  page = get_page(url)
  content = page.split()
  for word in content:
    add_to_index(word, index, url)

def get_page(url):
  try:
    import urllib.request
    page = urllib.request.urlopen(url).read()
    page = page.decode("utf-8")
    return page
  except:
    return ""

def get_next_target(page):
  startLink = page.find('<a href')
  if startLink == -1 :
    return None, 0
  startQuote = page.find('"', startLink+1)
  endQuote= page.find('"', startQuote+1 )
  url= page[startQuote+1: endQuote]
  return url, endQuote

def get_link(link):
  urlList=[]
  page = get_page(link)
  while True:
    url, endPos = get_next_target(page)
    if url:
      page=page[endPos:]
      urlList.append(url)
    else:
      break
  return urlList

def graph(myList):
  graph = {}
  for link in myList:
      graph[link] = get_link(link)
  return graph


def crawler_ranked(seed) :
  tocrawl = set([seed])
  crawled = set([])
  index = {}
  graph = {}
  while tocrawl:
    link = tocrawl.pop()
    if link not in crawled :
      add_page_to_index(index, link)
      tocrawl.update(get_link(link))
      crawled.add((link))
      graph[link] = get_link(link)
  rankIndex = compute_ranks(graph)
  return index, rankIndex
