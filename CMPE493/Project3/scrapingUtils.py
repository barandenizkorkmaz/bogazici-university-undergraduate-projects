from urllib.request import urlopen
import re
import os
import pickle

# Regex Patterns
titlePattern = r'<title>(.*) by (.*)<\/title>'
genrePattern = r'"shelf", (.*)\)'
authorPattern = r'<a class="authorName".*"name">(.*)</span></a>' # Enable multi-line
descPattern = r'<span id="(.*)">(.*</a>\))?(.*)</span>'
recommendationPattern = r"<li class='cover'(.+\n)+</a>"
recommendationURLPattern = r'<a href="(.*)"><'
recommendationBookNamePattern = r'<img alt="(.*)" src'

# Subpatterns within description block
smallDescStart = '<span id="freeTextContainer'
smallDescEnd = '</span>'
longDescStart = '<span id="freeText'
longDescEnd = '</span>'

# Reads the content of given file into a list.
def getBookURLs(fileName:str = 'books_toy.txt') -> list:
    urlList = list()
    with open(fileName,'r') as f:
        for line in f.readlines():
            urlList.append(line.strip())
    return urlList

# REFERENCE: https://realpython.com/python-web-scraping-practical-introduction/#scrape-and-parse-text-from-websites
# Returns the fetched content of book in the desired format.
# Returns: Dict (METADATA)
#   {
#       'TITLE': str,
#       'AUTHORS': list(str),
#       'DESC': str
#       'RECOMMENDATIONS': list(url) url -> <string>
#       'GENRES': list(str)
#   }
def fetchBookContent(url:str) -> dict:
    try:
        page = urlopen(url)
        print("URL: {} Status Code: {}".format(url,page.getcode()))
        while page.getcode() != 200:
            page = urlopen(url)
            print("URL: {} Status Code: {}".format(url, page.getcode()))
        html_bytes = page.read()
        page.close()
        html = html_bytes.decode("utf-8")
        book = {
            'TITLE': getTitle(html),
            'AUTHORS': getAuthors(html),
            'DESC': getDescription(html),
            'RECOMMENDATIONS': getRecommendations(html),
            'GENRES': getGenres(html)
        }
        return book
    except:
        print("Error: Could not fetch url data...")
        return None

# Returns title of a book from the given string of HTML input.
def getTitle(html:str) -> str:
    title = re.search(titlePattern, html).groups()[0]
    return title

# Returns the list of authors of a book from the given string of HTML input.
def getAuthors(html:str) -> list:
    authorsObject = re.compile(authorPattern, re.M)
    authors = authorsObject.findall(html)
    return authors

# Returns the description of a book from the given string of HTML input.
def getDescription(html:str) -> str:
    desc = str()
    descBody = html[html.find('<div id="description"'):]
    shortDescRaw = descBody[descBody.find(smallDescStart):descBody.find(smallDescEnd)+len(smallDescEnd)]
    shortDesc = cleanhtml(shortDescRaw)
    descBody = descBody[descBody.find(smallDescEnd)+len(smallDescEnd):]
    longDescRaw = descBody[descBody.find(longDescStart):descBody.find(longDescEnd)+len(longDescEnd)]
    longDesc = cleanhtml(longDescRaw)
    if len(longDesc) == 0:
        desc = shortDesc
    else:
        desc = longDesc
    return desc

# REFERENCE: https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
# Returns the plain text from a raw html by removing all html tags, etc.
def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

# Returns the list of recommendations of a book from the given string of HTML input.
def getRecommendations(html:str) -> list:
    res = list()
    recommendationsBody = html[html.find("<div id='{}".format("relatedWorks")):]
    recommendations = re.findall(recommendationPattern,recommendationsBody)
    for recommendation in recommendations:
        recomendationURL = re.search(recommendationURLPattern, recommendation).groups()[0]
        recommendationBookName = re.search(recommendationBookNamePattern, recommendation).groups()[0]
        res.append(recomendationURL)
    return res

# Returns the list of genres of a book from the given string of HTML input.
def getGenres(html:str) -> list:
    genresStr = re.search(genrePattern,html).groups()[0][1:-1]
    genreList = genresStr.split(',')
    genreList = [genre[1:-1] for genre in genreList]
    return genreList

"""
Returns the metadata structure that contains the fetched content for every book URL.
Input: List of book URLs.
Returns: Dict (METADATA)
    Key: String of Book URL
    Value: Dictionary of Book Content
      {
          'TITLE': str,
          'AUTHORS': list(str),
          'DESC': str
          'RECOMMENDATIONS': list(url) url -> <string>
          'GENRES': list(str)
      }
"""
def getMetadata(bookURLs:list) -> dict:
    metadata = dict()
    for i,url in enumerate(bookURLs):
        print("Processing URL id: ",i+1)
        content = fetchBookContent(url)
        if not content is None:
            metadata[url] = content
        else:
            print("Error Processing URL id: ",i+1)
    return metadata

# Saves the metadata file as 'metadataAss3.pickle'.
def saveMetadata(corpus:dict, fileName = 'metadataAss3.pickle'):
    with open(fileName, 'wb') as f:
        pickle.dump(corpus, f, protocol=pickle.HIGHEST_PROTOCOL)

# Deletes previously saved metadata file.
def deleteMetadata(fileName = 'metadataAss3.pickle'):
    try:
        os.system('rm {}'.format(fileName))
        print("Previously saved metadata deleted!")
    except FileNotFoundError as e:
        print("No previously saved metadata found!")

# Checks whether a previously saved metadata file exists.
def searchMetadata(fileName = 'metadataAss3.pickle'):
    return os.path.exists(fileName)