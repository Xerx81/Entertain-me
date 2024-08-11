import discord
import os
from dotenv import load_dotenv
from scraper import Scraper

if __name__ == "__main__":
  load_dotenv()
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  urls = {
    "top_movies": "https://www.imdb.com/chart/top/",
    "title": "https://www.imdb.com/search/title/?title=",
    "release": "https://www.imdb.com/search/title/?release_date=",
    "movies": "https://www.imdb.com/search/title/?title_type=feature",
    "series": "https://www.imdb.com/search/title/?title_type=tv_series",
    "games": "https://www.imdb.com/search/title/?title_type=video_game",
  }

  @client.event
  async def on_ready():
    print(f'We have logged in as {client.user}')

  @client.event
  async def on_message(message):

    if message.author == client.user:
      return

    if message.content.startswith('.topmovies'):
      url = urls['top_movies']
      scraper = Scraper()
      movie_msg = scraper.get_top_movies(url)
      await message.channel.send(f"```{movie_msg}```")

    if message.content.startswith('.movies'):
      url = urls['movies']
      scraper = Scraper()
      movie_msg = scraper.advanced_search(url)
      await message.channel.send(f"```{movie_msg}```")

    if message.content.startswith('.series'):
      url = urls['series']
      scraper = Scraper()
      movie_msg = scraper.advanced_search(url)
      await message.channel.send(f"```{movie_msg}```")

    if message.content.startswith('.games'):
      url = urls['games']
      scraper = Scraper()
      movie_msg = scraper.advanced_search(url)
      await message.channel.send(f"```{movie_msg}```")    

    if message.content.startswith('.title'):
      url = urls['title']
      title = ' '.join(message.content.split()[1:])
      full_url = f"{url}{title}"

      scraper = Scraper()
      movie_msg = scraper.advanced_search(full_url)
      await message.channel.send(f"```{movie_msg}```")

    if message.content.startswith('.release'):
      url = urls['release']
      release_year = ''.join(message.content.split()[1:])
      full_url = f"{url}{release_year}"

      scraper = Scraper()
      movie_msg = scraper.advanced_search(full_url)
      await message.channel.send(f"```{movie_msg}```")

    if message.content.startswith('.help'):
      commands_info = [
        ".topmovies - Gives list of top 5 movies of all time",
        ".movies - Gives list of top 5 currently popular movies",
        ".series - Gives list of top 5 currently popular series",
        ".games - Gives list of top 5 currently popular games",
        ".title item_name(e.g. star wars) - Gives list of top 5 items regarding the title",
        ".release item_year(e.g. 2024) - Gives list of top 5 items from given year"
        ]
      msg = f"Commands:-\n\n\n{'\n\n'.join(commands_info)}"
      await message.channel.send(f"```{msg}```")

  client.run(os.getenv('TOKEN'))

