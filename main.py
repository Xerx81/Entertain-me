import discord
import os
from dotenv import load_dotenv
from scraper import Scraper

if __name__ == "__main__":
  load_dotenv()

  urls = {
    "top_movies": "https://www.imdb.com/chart/top/",
    "title": "https://www.imdb.com/search/title/?title=",
  }

  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

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

    if message.content.startswith('.title'):
      url = urls['title']
      title = ' '.join(message.content.split()[1:])
      full_url = f"{url}{title}"

      scraper = Scraper()
      movie_msg = scraper.get_by_title(full_url)
      await message.channel.send(f"```{movie_msg}```")

  client.run(os.getenv('TOKEN'))

