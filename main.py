import discord
import os
from discord import app_commands
from dotenv import load_dotenv
from scraper import Scraper

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from a .env file

    # Define intents to specify which events your bot will receive
    intents = discord.Intents.default()
    intents.message_content = True  # Allow the bot to read message content

    # Create a client instance with the specified intents
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)  # Set up a command tree for slash commands

    urls = {
        "topmovies": "https://www.imdb.com/chart/top/",
        "movies": "https://www.imdb.com/search/title/?title_type=feature",
        "series": "https://www.imdb.com/search/title/?title_type=tv_series",
        "games": "https://www.imdb.com/search/title/?title_type=video_game",
        "title": "https://www.imdb.com/search/title/?title=",
        "release": "https://www.imdb.com/search/title/?release_date=",
    }

    scraper = Scraper()

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        try:
            synced = await tree.sync()  # Sync all commands
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            print(e)


    @tree.command()
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f'Hi, {interaction.user.mention}!')


    @tree.command(name="topmovies", description="Gives list of top 5 movies of all time")
    async def topmovies(interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['topmovies']
            movie_msg = scraper.get_top_movies(url)
            await interaction.followup.send(f"```{movie_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="movies", description="Gives list of top 5 currently popular movies")
    async def movies(interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['movies']
            movie_msg = scraper.advanced_search(url)
            await interaction.followup.send(f"```{movie_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="series", description="Gives list of top 5 currently popular series")
    async def series(interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['series']
            series_msg = scraper.advanced_search(url)
            await interaction.followup.send(f"```{series_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="games", description="Gives list of top 5 currently popular games")
    async def games(interaction: discord.Interaction):
        try:
            await interaction.response.defer(ephemeral=True)
            url = urls['games']
            games_msg = scraper.advanced_search(url)
            await interaction.followup.send(f"```{games_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="title", description="Gives list of top 5 items regarding the title")
    @app_commands.describe(item_name="The title to search for")
    async def title(interaction: discord.Interaction, item_name: str):
        try:
            await interaction.response.defer(ephemeral=True)
            url = f"{urls['title']}{item_name}"
            title_msg = scraper.advanced_search(url)
            await interaction.followup.send(f"```{title_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="release", description="Gives list of top 5 items from given year")
    @app_commands.describe(item_year="The release year to search for")
    async def release(interaction: discord.Interaction, item_year: int):
        try:
            await interaction.response.defer(ephemeral=True)
            url = f"{urls['release']}{item_year}"
            release_msg = scraper.advanced_search(url)
            await interaction.followup.send(f"```{release_msg}```")
        except Exception as e:
            print(e)


    @tree.command(name="help", description="Shows list of available commands")
    async def help(interaction: discord.Interaction):
        commands_info = [
            "/topmovies - Gives list of top 5 movies of all time",
            "/movies - Gives list of top 5 currently popular movies",
            "/series - Gives list of top 5 currently popular series",
            "/games - Gives list of top 5 currently popular games",
            "/title item_name - Gives list of top 5 items regarding the title",
            "/release item_year - Gives list of top 5 items from given year"
        ]
        msg = f"Commands:\n\n{'\n\n'.join(commands_info)}"
        await interaction.response.send_message(f"```{msg}```")

    # Run the bot using the token from the .env file
    client.run(os.getenv('TOKEN'))