from bs4 import BeautifulSoup as soup
import requests

# get the urls of todays articles
def get_bbc_world_links(url="https://www.bbc.com/news/world") -> list:
  html = requests.get(url)
  bsobj = soup(html.content, 'lxml')

  urls = []
  for link in bsobj.findAll("a", attrs={'class':'gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor'}):
    if '/news/world' in link['href']:
      required_url = 'https://www.bbc.com' + link['href']
      urls.append(required_url)
  
  # remove duplicate urls
  all_urls = list(set(urls))

  return all_urls

def get_article_headings(url:str) -> str:

  html = requests.get(url)
  bsobj = soup(html.content, 'lxml')

  heading = bsobj.find('h1', attrs={'id':'main-heading'}).text
  
  return heading

def get_article_contributors(url:str) -> str:

  html = requests.get(url)
  bsobj = soup(html.content, 'lxml')

  # to account for some articles not having contributors
  try:
    contributors = bsobj.find('div', attrs={'class':'ssrcss-68pt20-Text-TextContributorName e8mq1e96'}).text
    contributors_only = contributors.replace("By ", "")
    return contributors_only
  except:
    return ""
  
def get_article_body(url:str) -> str:

  html = requests.get(url)
  bsobj = soup(html.content, 'lxml')

  # get article body
  paragraphs = []
  for x in bsobj.findAll('div', attrs={'data-component':'text-block'}):
    content = x.text + '\n'
    paragraphs.append(content)
  full_text = "".join(paragraphs)

  return full_text

def get_bbc_page_contents(url:str) -> str:

  # get article headings
  heading = get_article_headings(url=url)

  # get name(s) of article's contributor(s)
  contributors = get_article_contributors(url=url)

  # get article body
  full_text = get_article_body(url=url)

  combined_text = 'Headline: ' + heading + '\n' + 'Contributor(s): ' + contributors + '\n' + full_text
  return combined_text

def articles_for_embeddings(url_list=None):
  if url_list is None:
    url_list = get_bbc_world_links()
  
  daily_reading = []
  for url in url_list:
    content = get_bbc_page_contents(url)
    spaced_content = content + '\n\n\n'
    daily_reading.append(spaced_content)

  full_text = "".join(daily_reading)

  return full_text

if __name__ == '__main__':
  articles = articles_for_embeddings()
  print(articles)