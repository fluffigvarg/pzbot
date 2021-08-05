#! /usr/bin/env python

from flutterbyIRC import flutterbyIRC
import time
import commands
import react

class ExampleBot(flutterbyIRC):
    def __init__(self):
        super().__init__()

        # Credentials:
        self.USERNAME  = ""         
        self.TOKEN     = "" # include oauth, like "oauth:<KEY>"
        self.CLIENT_ID = ""

        # List of channels to join, include the #:
        self.CHANNELLIST = [f"#"] # [f"#channel1",f"#channel2"]

        # Display RAW IRC to Console?
        self.ShowRAWOutput = False

        # Raw Log?        
        self.rawlogenabled = False   

    # Use this to add your own functions that are mapped to IRC events
    def register_event_handlers(self):
        self.add_handler("pubmsg", self.process_pub_message)
        self.add_handler("privmsg", self.send_message)

    def process_pub_message(self, connection, event):
        tags = {kvpair["key"]: kvpair["value"] for kvpair in event.tags}
        user = {"name": tags["display-name"], "id": tags["user-id"]}
        message = event.arguments[0]
        username = user['name']
        channel_name = event.target

        # Insert React processing function - pass bot, user, message, channel
        commands.process(MyBot, username, message, channel_name)
        react.process(MyBot, username, message, channel_name)

        # Print to console
        print(f"{username}: {message}")

        
    def send_message(self, channel, message):
        self.Connection.privmsg(channel, message)

if __name__ == '__main__':
    MyBot = ExampleBot()
    MyBot.connect()
