import discord
from discord import Webhook, RequestsWebhookAdapter
from pathlib import Path
import io
import aiohttp
from PIL import Image

client = discord.Client()

user_list={}
emojis={}
dled_emojis=[]

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    for guild in client.guilds:
        for emoji in guild.emojis:
            emojis[emoji.name] = emoji
    print (emojis)

@client.event
async def on_guild_join(guild):
    for emoji in guild.emojis:
        emojis[emoji.name] = emoji

@client.event
async def on_guild_emojis_update(guild, before, after):
    for emoji in after:
        emojis[emoji.name] = emoji

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$bye'):
        await message.channel.send('Good bye')
    if message.content.startswith('$areyousentient'):
        await message.channel.send(':( no.')
    if message.content.startswith('$canyoupredictthefuture'):
        await message.channel.send('What makes you think I can if you can\'t?')
    if message.content.startswith('$wth'):
        await message.channel.send(file=discord.File("memes/what to heck.png","whattoheck.png"))
    if message.content.startswith('$affleck'):
        await message.channel.send(file=discord.File("memes/affleck.png","affleck.png"))
    if message.content.startswith('$mtta'):
        await message.channel.send(file=discord.File("memes/mtta.jpg","mtta.jpg"))
    if message.content.startswith('$itp'):
        await message.channel.send(file=discord.File("memes/inthisphoto.jpg","inthisphoto.jpg"))



    if ".." in message.content:
        author = message.author
        name = author.display_name
        avatar = author.avatar_url
        weblist = await message.channel.webhooks()
        counter = 0
        sender = "```ini\n[ " + name + " ( # " + author.name + str(author.discriminator) + " )] #" + \
                 str(message.created_at.strftime("%Y-%m-%d %H:%M")) + ": ```"
        for hook in weblist:
            if hook.name == "emojibot":
                counter = + 1
                webhook = hook
            else:
                counter = + 0
        if counter == 0:
            webhook = await message.channel.create_webhook(name="emojibot")
        start = message.content.find("..")
        end = message.content.rfind("..")
        emoji = message.content[start + len(".."):end]
        jumbocounter = 0
        extracounter = 0
        folder = "emojis"

        if emoji[0:2] ==".j":
            jumbocounter = 1
            extracounter = 0
            emoji = emoji.replace(".j","")
        elif emoji[0:2] ==".e":
            jumbocounter = 0
            extracounter = 1
            emoji = emoji.replace(".e","")
        else:
            jumbocounter = 0
            extracounter = 0

        emoji_str = "<:" + emoji + ":" + str(emojis[emoji].id) + ">"

        if emoji in emojis and emoji not in dled_emojis:
            # await emojis[emoji].url.save(folder + "/" + emoji+".png")
            # image = Image.open(folder + "/" + emoji + ".png")
            # image.thumbnail((48, 48))
            # image.save(folder + "/48/" + emoji+".png")
            # image.thumbnail((22 , 22))
            # image.save(folder + "/22/" + emoji + ".png")
            dled_emojis.append(emoji)

        if emoji in dled_emojis:
            if jumbocounter == 1:
                await message.delete()
                embed = discord.Embed(description = sender, colour = author.color)
                embed.set_thumbnail(url = str(author.avatar_url_as(size=32)))
                embed.set_image(url = str(emojis[emoji].url))
                await message.channel.send(embed = embed)

            elif extracounter == 1:
                await message.delete()
                embed = discord.Embed(title = emoji_str * (int(256/len(emoji_str))),
                                      description = emoji_str*(int(2048/len(emoji_str))),
                                      colour = author.color)
                embed.set_author(name = sender[7:-3],icon_url = str(emojis[emoji].url))
                embed.set_thumbnail(url = str(author.avatar_url_as(size=32)))
                embed.set_footer(text= emoji ,icon_url=str(emojis[emoji].url))
                embed.set_image(url = str(emojis[emoji].url))
                embed.add_field(name=emoji_str * (int(256/len(emoji_str))), value=emoji_str*(int(1024/len(emoji_str))),
                                inline=True)
                embed.add_field(name=emoji_str * (int(256/len(emoji_str))), value=emoji_str*(int(1024/len(emoji_str))),
                                inline=True)
                await message.channel.send(content = emoji_str * 5 ,embed = embed)
                await message.channel.send(emoji_str * 5)


            elif len(message.content) == len(emoji) + 4:
                await message.delete()
                embed = discord.Embed(description = sender, colour = author.color)
                embed.set_thumbnail(url = str(author.avatar_url_as(size=32)))
                # embed.set_image(url = str(emojis[emoji].url))
                #file = discord.File(folder + "/48/" + emoji+".png", filename="image.png")
                await message.channel.send(embed = embed)
                await message.channel.send(emoji_str)
            else:
                await message.delete()
                embed = discord.Embed(description=sender, colour=author.color)
                embed.set_thumbnail(url=str(author.avatar_url_as(size=32)))
                content = message.content.replace(".."+emoji+"..", emoji_str)
                await message.channel.send(embed = embed)
                await message.channel.send(content)

    if message.content.startswith('$semojilist'):
        for emoji in message.guild.emojis:
            await message.channel.send( '<:'+ emoji.name +':'+str(emoji.id)+'> `..'+ emoji.name +'..`')


client.run('Njc3NDYyMjUyNTA4Njc2MTAz.XkUnyQ.vvfmTY9ziJxwo4zbyVS8y-t3CVA')
# def make_webhook(name,avatar,content):
#
#     name = ### get user name in guild
#     avatar = ### get user avatar in guild
#     content = ### get emoji to be used
#image = Image.open(folder + "/" + emoji+".png")
#     Webhook.send(content=,username=,avatar_url=,) C:/Users/allie/PycharmProjects/emoji bot/venv/Scripts


    ###send(content=None, *, wait=False, username=None, avatar_url=None, tts=False, file=None, files=None, embed=None, embeds=None)¶
###https://discordapp.com/api/oauth2/authorize?client_id=677662208397672478&permissions=2146954608&scope=bot


# data.save(folder + "/" + emoji+".png", "PNG")
# data.seek(0)
# image = data.read()
# dataBytesIO = io.BytesIO(image)
# Image.open(dataBytesIO)
# print ( data, image, dataBytesIO )
# dled_emojis[emoji] = data
# size = (128, 128)
# image = data.thumbnail(size)
# image.save(folder + "/" + emoji+".png")

'''
            f = open("emojis\myfile.txt", "x")
            emojiimg = await emojis[emoji].url.save(folder)'''

# py -3 eb.py