import discord
import os
from dotenv import load_dotenv
from scraper import Scraper

if __name__ == "__main__":
  load_dotenv()
  intents = discord.Intents.default()
  intents.message_content = True
  client = discord.Client(intents=intents)

  search_commands = {
    ".topmovies": "https://www.imdb.com/chart/top/",
    ".movies": "https://www.imdb.com/search/title/?title_type=feature",
    ".series": "https://www.imdb.com/search/title/?title_type=tv_series",
    ".games": "https://www.imdb.com/search/title/?title_type=video_game",
    ".title": "https://www.imdb.com/search/title/?title=",
    ".release": "https://www.imdb.com/search/title/?release_date=",
  }

  @client.event
  async def on_ready():
    print(f'We have logged in as {client.user}')

  @client.event
  async def on_message(message):

    if message.author == client.user:
      return

    if message.content.startswith('.'):
      command = message.content.split()[0].lower()

      if command in search_commands:
        url = search_commands[command]
        scraper = Scraper()

        if command == '.topmovies':
          movie_msg = scraper.get_top_movies(url)
          await message.channel.send(f"```{movie_msg}```")

        elif command == '.title' or command == '.release':
          input = ' '.join(message.content.split()[1:])
          full_url = f"{url}{input}"

          movie_msg = scraper.advanced_search(full_url)
          await message.channel.send(f"```{movie_msg}```")
  
        else:
          movie_msg = scraper.advanced_search(url)
          await message.channel.send(f"```{movie_msg}```")

      elif command == '.help':
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

      else:
        await message.channel.send("```Invalid Command! Use '.help' for a list of commands.```")

  client.run(os.getenv('TOKEN'))