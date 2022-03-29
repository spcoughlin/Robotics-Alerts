'''
Computer Programming Quarter 3 Project - Robotics Discord Bot

Written by Sean Coughlin

Email References:
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
from discord_calendar import DiscordCalendar

bot = commands.Bot(command_prefix='.')
bot_calendar = DiscordCalendar()

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
    await bot.process_commands(message)

# -- COMMANDS --

@bot.command()
async def config_channel(ctx):
    global fixed_channel
    fixed_channel = discord.utils.get(ctx.guild.text_channels, name="generaled")
    await fixed_channel.send('Email Channel Configured to {}'.format("generaled")) 

@bot.command()
async def commands_list(ctx):
    await ctx.channel.send("Commands: \n.config_channel - configure the channel to send email updates in \n.commands_list - Brings up this pannel \n.website - Links the hours website \n.add_event <month, day, year, 'event'> - add an event to the calendar. Do not include the brackets, but include the apostrophes on 'event' for a multi-word description. \n.calendar - show the calendar \n.clear_calendar - wipes the calendar; can only be used by members with the 'administrator' permission ")

@bot.command()
async def website(ctx):
    await ctx.channel.send("https://arvigo6015.pythonanywhere.com/")

@bot.command()
async def add_event(ctx, month, day, year, event):

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
    await ctx.channel.send(bot_calendar.compile_calendar())
    
@bot.command()
async def clear_calendar(ctx):
    '''
    This can only be run by members with the 'administrator' permission
    '''
    if ctx.author.guild_permissions.administrator or ctx.author.name == "iiPanCake":
        with open("calendar.txt",'w') as f: # clear file 
            pass
        await ctx.channel.send("Cleared Calendar")
    else:
        await ctx.channel.send("Insufficient Permissions")

# -- END COMMANDS -- 

async def emailer():
    '''
    This is the daemon function for email updates. 

    Make sure to run it on a separate thread!
    '''

    f = open("config_email.txt", "r")
    config_email_list = f.readlines()

    username = config_email_list[0]
    password = config_email_list[1]
    email1 = config_email_list[2]
    email2 = config_email_list[3]
    alert_message = config_email_list[4]

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

                    if From == email1 or From == email2:
                        await fixed_channel.send(alert_message)

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
