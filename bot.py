# This example requires the 'message_content' intent.
import csv
import discord
import json
from random import randint
from discord import app_commands
from image import create_quote_image

# Token
try:
    f = open('token.json')
    TOKEN = json.load(f)["token"]
    f.close()
except Exception as e:
    print(f"Error loading token: {e}")

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Saving all entries into list
quotes=[]
authors=[]
tags=[]

try:
    with open("quotes/scraping_quotes.csv", encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            quotes.append(row[0])
            authors.append(row[1])
            tags.append(row[2])

except Exception as e:
    print(f"Error loading quotes: {e}")

# Number of entries
num_entries = len(quotes)

# Create quote from user input
@tree.command(
    name="create-quote",
    description="generate an image with your quote!",
    guild=discord.Object(id=1135007978857189511)
)
@app_commands.describe(quote="The quote")

async def create_quote(interaction: discord.Interaction, quote: str):
    # Format text
    quote = f'"{quote}"'
    author = interaction.user.name

    # Create image and embed
    image_url = f"images/quote_{interaction.user.name}.png"
    create_quote_image(quote, author, image_url)


    with open(image_url, 'rb') as file:
        picture = discord.File(file)
        await interaction.response.send_message(file=picture)


# Send a random quote
@tree.command(
        name = "random-quote",
        description = "get a random quote to motivate yourself!",
        guild=discord.Object(id=1135007978857189511)
)
async def random_quote(interaction: discord.Interaction):
    rand_num = randint(0,num_entries-1)

    image_url = f"images/quote_{interaction.user.name}_random.png"
    create_quote_image(quotes[rand_num], authors[rand_num], image_url)

    with open(image_url, 'rb') as file:
        picture = discord.File(file)
        await interaction.response.send_message(file=picture)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await tree.sync(guild=discord.Object(id=1135007978857189511))

client.run(token=TOKEN)
