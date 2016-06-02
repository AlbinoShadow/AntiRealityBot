# Import some necessary libraries.
import irc.client
import irc.connection
#import irc.bot
import ssl
import sqlite3
import datetime
import time 

# Some basic variables used to configure the bot
channel0 = "##wat" # Channel0
channel1 = "#home" # Chanel1
botnick = "PlsStopBanningMe" # Your bots nick
identify_string = "identify password"

prefix = "-fake"

def on_connect(connection, event):
   connection.privmsg("nickserv", identify_string)
   connection.join(channel0)

def on_msg(connection, event):
    for a in event.arguments:
       do_command(connection, event.source, event.target, a)

def on_kick(connection, event):
    if nick == botnick:
       connection.join(channel0)
    else:
       return

def do_command(connection, source, target, commandline):
   output = None
   cl_list = commandline.split(" ", 2)

   if cl_list[0].lower() == "what":
   	  output = "wat* "

   elif cl_list[0].lower() == "wat":
      # The @ must be there, irc standard
      host = source.split("@")[1]

      host_split = host.split("/")

      if len(host_split) < 3:
         return
   
      # Only allow nickserved users
      if host_split[0] != "tripsit":
         return

      #nick = host_split[2]
      nick = source.split("!", 1)[0]
   
      if target == botnick:
         target = nick

      output = nick + "++"

   else:
      if len(cl_list) < 2:
         return

      if cl_list[0].lower() != prefix:
         return

      command = cl_list[1].lower()
      if len(cl_list) > 2:
         args_list = cl_list[2].split(" ")
      else:
         args_list = []

      # The @ must be there, irc standard
      host = source.split("@")[1]

      host_split = host.split("/")

      if len(host_split) < 3:
         return
   
      # Only allow nickserved users
      if host_split[0] != "tripsit":
         return      

      #nick = host_split[2]
      nick = source.split("!", 1)[0]
   
      if target == botnick:
         target = nick

      if command == "leave":
         if nick == "Bjorn":
            output = "nope bear lover"
         elif nick != "Sp00ky":
            output = "nope llama lover"
         else:
            conn.close()
            connection.disconnect()
            raise SystemExit()
   
   if not output is None:   
      connection.privmsg(target, output)

def on_disconnect(connection, event):
   raise SystemExit()


ssl_factory = irc.connection.Factory(wrapper=ssl.wrap_socket)
client = irc.client.Reactor()
server = client.server()

server.connect(
   "chat.tripsit.me", 
   6697, 
   botnick, 
   username = botnick, 
   ircname = prefix + " help", 
   connect_factory = ssl_factory
)

client.add_global_handler("welcome", on_connect)
client.add_global_handler("privmsg", on_msg)
client.add_global_handler("pubmsg", on_msg)
client.add_global_handler("disconnect", on_disconnect)

client.process_forever()
