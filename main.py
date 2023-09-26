import discord
from discord.ext import commands
import os
from flask import Flask, request, render_template

from threading import Thread
from chemical_data import chemical_data  # Import the chemical_data dictionary
import json
allowed_command_channels = [1028680582156259428]  # Add your channel IDs here
allowed_command_channelsorder = [1028680582156259428]  # Add your channel IDs here
def is_allowed_channel(ctx):
    return ctx.channel.id in allowed_command_channels
def is_allowed_channelorder(ctx):
    return ctx.channel.id in allowed_command_channelsorder
try:
    with open("registered_users.json", "r") as f:
        registered_users = json.load(f)
except FileNotFoundError:
    registered_users = {}


class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        help_data = "\n".join(command.name for command in self.context.bot.commands)
        embed = discord.Embed(title="Help!!! Command List", description=help_data, color=0x00ff00)
        await destination.send(embed=embed)



app = Flask(__name__)
bot = commands.Bot(command_prefix='!')
bot.help_command = MyNewHelp()
@bot.command()
async def chemical(ctx, *, chemical_name):
    chemical_name = chemical_name.upper()
    
    if chemical_name in chemical_data:
        info = chemical_data[chemical_name]
        embed = discord.Embed(title=chemical_name, description=info, color=0xe74c3c)
        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Sorry, I don't have information for {chemical_name}.")

@bot.command()
@commands.check(is_allowed_channel)
async def chemicals(ctx):
    chemical_names = "\n".join(chemical_data.keys())
    embed = discord.Embed(title="Available Chemicals", description=chemical_names, color=0x00ff00)
    await ctx.send(embed=embed)
# Create an empty list to store registered users
registered_users = {} 

@bot.command()
@commands.check(is_allowed_channelorder)
async def order(ctx):
    user_id = ctx.author.id
    if user_id not in registered_users:
        # Register the user

        # registered_users[user_id] = {
        #     "name": str(ctx.author),
        #     "contact": contact_number.content,
        #     "products": [],
        #     "quantity": []
        # }
  
        await ctx.send("You have been registered for ordering. Please check your private messages for instructions.")

        user = ctx.author
        dm_channel = await user.create_dm()
        await dm_channel.send("Welcome to the order channel! Please provide the following information:")
        
        # Ask for contact number
        await dm_channel.send("Please enter your contact number:")
        contact_number = await bot.wait_for('message', check=lambda message: message.author == user)
        
        await dm_channel.send("Please enter the product name:")
        product_name = await bot.wait_for('message', check=lambda message: message.author == user)
        
        await dm_channel.send("Please enter the quantity in tons:")
        quantity = await bot.wait_for('message', check=lambda message: message.author == user)
        await dm_channel.send("Thank You For Order We Will Inform You In Sort Tme That Your Order Is Confermered Or Not")
        registered_users[user_id] = {
            "name": str(ctx.author),
            "contact": str(contact_number.content),
            "orders": []  # Use a list to store orders
        }
        new_order = {
            "product": product_name.content,
            "quantity": quantity.content
        }
        registered_users[user_id]["orders"].append(new_order)
        
        with open("registered_users.json", "w") as f:
          json.dump(registered_users, f, indent=4)

      

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@app.route('/')
def bot_loaded():
    return "Bot has been loaded!"
@app.route('/data')
def display_users():
    # Read data from the registered_users.json file
    with open('registered_users.json', 'r') as json_file:
        data = json.load(json_file)
    
    # Render the template and pass the data to it
    return render_template('index.html', users=data)
def run():
    app.run(host='0.0.0.0', port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()

# Run the bot
keep_alive()
bot.run("MTA5ODk5Mzc3ODA0NTUwNTU5Nw.GwaVSZ.mFOUmz6ZmMprlV4-zbMSaWPV7I8y6BFetwbbpI")
