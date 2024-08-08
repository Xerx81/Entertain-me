import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

headers = {"User-Agent": "Mozilla/5.0"}

def scrape_imdb_top_5():
  url = "https://www.imdb.com/chart/top/"
  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")

  htmlTitle = soup.findAll(class_="ipc-title__text")

  i = 0
  titles = []
  exceptionalKeywords = ["IMDb", "Recently viewed"]
  for title in htmlTitle:
    if i == 5:
      break
    title = title.string
    if any(keyword in title for keyword in exceptionalKeywords):
      pass
    else:
      titles.append(title.string)
      i += 1
  return titles


def scrape_imdb_top_5_by_title():
  title = quote(input("Search by title: "))
  url = f"https://www.imdb.com/search/title/?title={title}"

  response = requests.get(url, headers=headers)
  soup = BeautifulSoup(response.content, "lxml")
  
  movie_containers = soup.findAll("li", class_="ipc-metadata-list-summary-item")

  i = 0
  movies = []
  for container in movie_containers:
    if i == 5:
     break
    title = container.find("h3", class_="ipc-title__text").text
    try:
      rating = container.find("span", class_="ipc-rating-star--rating").text
    except AttributeError:
      rating = "N/A"
    try:
      year = container.find("span", class_="sc-b189961a-8 hCbzGp dli-title-metadata-item").text
    except AttributeError:
      year = "N/A"

    movie = {
      "title": title,
      "rating": rating,
      "year": year
    }
    movies.append(movie)

    i += 1

  return movies
  
  
if __name__ == "__main__":
  # scrape_imdb_top_5()
  movies = scrape_imdb_top_5_by_title()
  for movie in movies:
    print(f"\n{movie['title']}\n{movie['year']}  ⭐ {movie['rating']}\n\n")

