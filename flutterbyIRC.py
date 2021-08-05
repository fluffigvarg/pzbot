#
# Simple Twitch/IRC Bot Example
#
# Connects to one or more Twitch chat channels and dumps events to console
#
# RFC for IRC: https://tools.ietf.org/html/rfc1459
# TwitchIRC Docs: https://dev.twitch.tv/docs/irc/guide
# Best Python IRC Examples/Lib: https://github.com/jaraco/irc
# IRCv3 Capabilities Explanation (used by Twitch heavily): https://ircv3.net/specs/core/capability-negotiation.html
#

import sys
import ssl
import irc.client

import requests
from requests import get

from datetime import datetime
import time

class SimpleServerConnection(irc.client.ServerConnection):
    
    def __init__(self, reactor):
        super().__init__(reactor)
        self.OUTPUT_TO_CONSOLE = False
        self.send_callback = self.do_nothing
        self.recv_callback = self.do_nothing

    def send_raw(self, string):
        if (self.OUTPUT_TO_CONSOLE):
            print(f"< {string}")
        self.send_callback(string)
        super().send_raw(string)

    def _process_line(self, string):
        if (self.OUTPUT_TO_CONSOLE):
            print(f"> {string}")
        self.recv_callback(string)
        super()._process_line(string)

    def do_nothing(self,string):
        pass

class SimpleReactor(irc.client.Reactor):
    connection_class = SimpleServerConnection

#
class flutterbyIRC():

    # init function to create this object (does not autostart)
    def __init__(self):

        # Credentials:
        self.USERNAME  = ""
        self.TOKEN     = "" # include oauth, like "oauth:<KEY>"
        self.CLIENT_ID = ""

        # List of channels to join, include the #:        
        self.CHANNELLIST = []

        # Connection Object
        self.Connection = None

        # Display RAW IRC to Console?
        self.ShowRAWOutput = True

        # Raw Log?        
        self.rawlogenabled = True        
        
        # Raw log filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        self.rawlogfile = f"raw_{timestamp}.log"

        # TwitchUserData
        self.TwitchUserData = None

    # Main function to boot and start this object
    def connect(self):
	
        # Auth to Twitch:
        print("\n==> Auth'ing to Twitch...")
        
        # Make HTTPS Call to API endpoint to login:
        url = f"https://api.twitch.tv/kraken/users?login={self.USERNAME}"
        headers = {"Client-ID": self.CLIENT_ID, "Accept": "application/vnd.twitchtv.v5+json"}
        try:
            self.TwitchUserData = get(url, headers=headers)
            self.TwitchUserData.raise_for_status() # treat response that has an error as an exception and throw it
            self.TwitchUserData = self.TwitchUserData.json()
        except requests.exceptions.HTTPError as err:
            # Soft error- like access denied
            print("==> ERROR!")
            raise SystemExit(err)  
        except requests.ConnectionError as err:
            # Hard error- like connection refused, or timeout
            print("==> ERROR!")
            raise SystemExit(err)

        print(f"==> Response from Twitch: {self.TwitchUserData}")
        
        # Spin up IRC over SSL and connect
        try:
            # Create an IRC-aware event handler that can grab IRC events off the wire and map them to function calls
            IRCEventSystem = SimpleReactor()

            # Create an SSL Object to handle our connection:
            ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)

            # Ask our IRC-aware object to connect using our SSL object (so we are encrypted)
            self.Connection = IRCEventSystem.server().connect(
                "irc.chat.twitch.tv", 6697, self.USERNAME, self.TOKEN, self.USERNAME, self.USERNAME, connect_factory=ssl_factory
            )
        except irc.client.ServerConnectionError:
            # If we're here, we've got an exception- dump it to the screen and throw an exit so we quit safely
            print(sys.exc_info()[1])
            raise SystemExit(1)

        # Connection should be ok from here on down

        # Enable Console Output? (we do this late so auth detials aren't exposed)
        if (self.ShowRAWOutput):
            self.Connection.OUTPUT_TO_CONSOLE = True

        print(f"==> Twitch IRC Server connected: {self.Connection.connected}")

        # Map IRC 'events' to functions that accept and do something with them
        print("==> Registering handlers...")
        self._register_event_handlers()    
        self.register_event_handlers()  

        # Ask out IRC-aware object to sit and listen forever
        print("==> Listening...")
        IRCEventSystem.process_forever()

    def add_handler(self, event, handler, priority=0):
        self.Connection.add_global_handler(event, handler, priority)

    # Register required handlers
    def _register_event_handlers(self):
        self.register_recv_handler(self.recv_handler)                
        self.register_send_handler(self.send_handler)
        self.add_handler("welcome", self.on_connect)
        self.add_handler("disconnect", self.on_disconnect)

    # Use this in child classes to map functions to different IRC events
    def register_event_handlers(self):
        pass

    def register_send_handler(self, handler):
        self.Connection.send_callback = handler

    def register_recv_handler(self, handler):
        self.Connection.recv_callback = handler

    def send_handler(self, string):
        if (self.rawlogenabled == True):
            message_timestamp = datetime.now()
            with open(self.rawlogfile, 'a+', encoding="utf-8") as file_object:
                file_object.write(f"{message_timestamp} < {string}\n")

    def recv_handler(self, string):
        if (self.rawlogenabled == True):
            message_timestamp = datetime.now()
            with open(self.rawlogfile, 'a+', encoding="utf-8") as file_object:
                file_object.write(f"{message_timestamp} > {string}\n")

    def on_connect(self,connection, event):
        for requestedCapability in ("membership", "tags", "commands"):
            connection.cap("REQ", f":twitch.tv/{requestedCapability}")
        for channel in self.CHANNELLIST:
            if irc.client.is_channel(channel):
                connection.join(channel)                
        return

    def on_disconnect(self,connection, event):
        print("==> Disconnect.")
        raise SystemExit()