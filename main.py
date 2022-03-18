import discord
import imaplib
import email
from email.header import decode_header
import smtplib
import datetime

config_key = "v@f82f82f8v@2f8"  # send this in the channel you want to configure bot

client = discord.Client()  # creates new discord bot


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):  # called every time a message is sent, even the bot's own message

    if message.content.startswith(config_key):  # sets the channel the bot will send updates in
        global fixed_channel
        fixed_channel = discord.utils.get(message.guild.text_channels, name="general")
        name = fixed_channel.name
        await fixed_channel.send('Channel Configured to {}'.format(name))

        global config_message
        global channel_configured
        config_message = message
        channel_configured = True

        await config_message.clear_reactions()

    if message.content.startswith(".help"):
        await message.channel.send("Commands: | .help - Brings up this panel | .website - links the hours website |")

    if message.content.startswith(".website"):
        await message.channel.send("https://arvigo6015.pythonanywhere.com/")


    # after the channel has been set, the bot starts searching for emails with this account
    username = "roboticsalerts@gmail.com"
    password = "R0b0t1cs"

    while True:
        # create an IMAP4 class with SSL
        imap = imaplib.IMAP4_SSL("imap.gmail.com")
        # authenticate
        imap.login(username, password)

        status, messages = imap.select("INBOX")
        # number of top emails to fetch
        N = 1
        # total number of emails
        messages = int(messages[0])

        for i in range(messages, messages - N, -1):
            # fetch the email message by ID
            res, msg = imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = str(subject.decode(encoding))
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = str(From.decode(encoding))

                    if From == "Samantha Delaney <samantha.delaney@bchigh.edu>" or From == "Sean Coughlin <56spc56@gmail.com>":
                        await fixed_channel.send("@everyone, Mrs. Delaney has sent an email. You should go read it!")

                        # here the bot sends an email to itself so it only pings once
                        server = smtplib.SMTP('smtp.gmail.com', 587)
                        server.starttls()
                        server.login(username, password)
                        SUBJECT = "Subject"
                        TEXT = "Text"

                        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

                        server.sendmail(username, username, message)
                        server.quit()

        # close the connection and logout
        imap.close()
        imap.logout()

client.run('OTQxNzU0NDQ5MTQyMDk1OTcz.YgajLQ.GIMnVRdznOPsnkShpB_EXLcMdBk')
