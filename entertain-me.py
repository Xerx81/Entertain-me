import requests
from bs4 import BeautifulSoup

def scrape_imdb_top_5():
  url = "https://www.imdb.com/chart/top/"
  headers = {"User-Agent": "Mozilla/5.0"}
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")
  htmlTitle = soup.findAll(class_="ipc-title__text")
  
  i = 0
  for title in htmlTitle:
    if i == 5:
      break
    title = title.string
    if "IMDb" in title or "Recently viewed" in title:
      pass
    else:
      print(title.string)
      i += 1
    

if __name__ == "__main__":
  scrape_imdb_top_5()
