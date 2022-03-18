'''
Computer Programming Quarter 3 Project - Robotics Discord Bot

Written by Sean Coughlin

Adapted From:
https://www.thepythoncode.com/article/reading-emails-in-python
https://realpython.com/python-send-email/#starting-a-secure-smtp-connection
'''

import discord
from discord.ext import commands
import imaplib
import email
from email.header import decode_header
import smtplib
import asyncio
import threading
from calendarx import CalendarX

config_key = "v@f82f82f8v@2f8"

bot = commands.Bot(command_prefix='$')

bot_calendar = CalendarX()

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))

    

    def functionInNewThread():
        loop = asyncio.new_event_loop()
        loop.run_until_complete(emailer())

    thread = threading.Thread(target=functionInNewThread, daemon=True)
    thread.start()

@bot.event
async def on_message(message): 

    if message.content.startswith(config_key):
        global fixed_channel
        fixed_channel = discord.utils.get(message.guild.text_channels, name="generaled")
        name = fixed_channel.name
        await fixed_channel.send('Email Channel Configured to {}'.format(name))      

    if message.content.startswith("help"):
        await message.channel.send("Commands: | .help - Brings up this panel | .website - links the hours website |")

    if message.content.startswith("website"):
        await message.channel.send("https://arvigo6015.pythonanywhere.com/")
    
    await bot.process_commands(message)

@bot.command()
async def addevent(ctx, month, day, year, event):

    print("addevent command detected")

    try: month = int(month)
    except: await ctx.channel.send("'month' parameter is not an int!")

    try: day = int(day)
    except: await ctx.channel.send("'day' parameter is not an int!")

    try: year = int(year)
    except: await ctx.channel.send("'year' parameter is not an int!")

    try: event = str(event)
    except: await ctx.channel.send("'event' parameter is not a string!")

    bot_calendar.add_date(month, day, year, event)

    await ctx.channel.send(f"{month, day, year} event added!")

@bot.command()
async def calendar(ctx):

    print("calendar command detected")

    await ctx.channel.send(bot_calendar.compile_calendar())
    
@bot.command()
async def clear_calendar(ctx):
    '''
    This can only be run by members with the 'administrator' permission
    '''
    if ctx.author.guild_permissions.administrator:
        with open("calendar.txt",'w') as f: # clear file 
            pass
        await ctx.channel.send("Cleared Calendar")
    else:
        await ctx.channel.send("Insufficient Permissions")

async def emailer():
    
    username = "roboticsalerts@gmail.com"
    password = "R0b0t1cs"

    while True:

        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        imap.login(username, password)
        status, messages = imap.select("INBOX")
        N = 1
        messages = int(messages[0])

        for i in range(messages, messages - N, -1):

            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    msg = email.message_from_bytes(response[1])
                    subject, encoding = decode_header(msg["Subject"])[0]

                    if isinstance(subject, bytes):
                        subject = str(subject.decode(encoding))

                    From, encoding = decode_header(msg.get("From"))[0]

                    if isinstance(From, bytes):
                        From = str(From.decode(encoding))

                    if From == "Samantha Delaney <samantha.delaney@bchigh.edu>" or From == "Sean Coughlin <56spc56@gmail.com>":
                        await fixed_channel.send("@everyone, Mrs. Delaney has sent an email. You should go read it!")

                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(username, password)
                        SUBJECT = "Subject"
                        TEXT = "Text"

                        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

                        server.sendmail(username, username, message)
                        server.quit()

        imap.close()
        imap.logout()

bot.run('OTQxNzU0NDQ5MTQyMDk1OTcz.YgajLQ.GIMnVRdznOPsnkShpB_EXLcMdBk')
