import requests
from bs4 import BeautifulSoup

class Scraper:
    headers = {"User-Agent": "Mozilla/5.0"}
    common_list_tag = ("li", {"class": "ipc-metadata-list-summary-item"})
    common_title_tag = ("h3", {"class": "ipc-title__text"})
    common_rating_tag = ("span", {"class": "ipc-rating-star--rating"})
    common_year_tag = ("span", {"class": "sc-b189961a-8 hCbzGp dli-title-metadata-item"})
    
    def get_soup(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=10) 
            return BeautifulSoup(response.content, "lxml")
        except requests.RequestException as e:
            print(f"Request error: {e}")
            return None
    
    def scrape(self, soup, list_tag, title_tag, rating_tag, year_tag):
        if soup is None:
            return []
        
        movie_containers = soup.findAll(*list_tag)
        movies = []
        
        for container in movie_containers[:5]:
            movie = {}
            title = container.find(*title_tag)
            movie['title'] = title.text if title else "N/A"
            
            rating = container.find(*rating_tag)
            movie['rating'] = rating.text if rating else "N/A"
            
            year = container.find(*year_tag)
            movie['year'] = year.text if year else "N/A"
            
            movies.append(movie)
        
        return movies
    
    def dict_to_string(self, movies):
        if not movies:
            return "No Results! Try again."
        
        return "\n".join(
            f"{movie['title']}\n{movie['year']}  ⭐{movie['rating']}\n\n"
            for movie in movies
        ).strip()
    
    def get_top_movies(self, url):
        soup = self.get_soup(url)
        year_tag = ("span", {"class": "sc-b189961a-8 hCbzGp cli-title-metadata-item"})
        
        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, year_tag)
        return self.dict_to_string(movies)
    
    def advanced_search(self, url):
        soup = self.get_soup(url)
        
        movies = self.scrape(soup, self.common_list_tag, self.common_title_tag, self.common_rating_tag, self.common_year_tag)
        return self.dict_to_string(movies)