import requests
from bs4 import BeautifulSoup

class Scraper:
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}
        self.common_list_tag = ("li", {"class": "ipc-metadata-list-summary-item"})
        self.common_title_tag = ("h3", {"class": "ipc-title__text"})
        self.common_rating_tag = ("span", {"class": "ipc-rating-star--rating"})
        self.common_year_tag = ("span", {"class": "sc-b189961a-8 hCbzGp dli-title-metadata-item"})

    def get_soup(self, url):
        response = requests.get(url, headers=self.headers)
        return BeautifulSoup(response.content, "lxml")
    
    def scrape(self, soup, list_tag, title_tag, rating_tag, year_tag):
        movie_containers = soup.findAll(*list_tag)

        movies = []
        for container in movie_containers[:5]:
            try:
                title = container.find(*title_tag).text
            except AttributeError:
                title = "N/A"
            try:
                rating = container.find(*rating_tag).text
            except AttributeError:
                rating = "N/A"
            try:
                year = container.find(*year_tag).text
            except AttributeError:
                year = "N/A"

            movie = {
            "title": title,
            "rating": rating,
            "year": year
            }
            movies.append(movie)
        return movies
    
    def dict_to_string(self, movies):
        movie_msg = ""
        for movie in movies:
            movie_msg += f"{movie['title']}\n{movie['year']}  ⭐{movie['rating']}\n\n"
        
        if movie_msg:
            return movie_msg
        else:
            print(movie_msg)
            return "No Results! Try again."
    
    def get_top_movies(self, url):
        soup = self.get_soup(url)
        list_tag = ("li", {"class": "ipc-metadata-list-summary-item sc-10233bc-0 TwzGn cli-parent"})
        year_tag = ("span", {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"})

        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, year_tag)
        movie_msg = self.dict_to_string(movies)
        return movie_msg
    
    def get_by_title(self, url):
        soup = self.get_soup(url)

        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, self.common_year_tag)
        movie_msg = self.dict_to_string(movies)
        return movie_msg
    