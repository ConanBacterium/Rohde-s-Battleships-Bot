__author__ = 'rohdehoved'

import socket
import threading

class IrcClient(threading.Thread):
    #basic stuff
    server = "irc.freenode.net"
    channel = "#BattleshipsFIGHTGOGO"
    botnick = "MegaBattleShipsBlaster3000"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #Function for sending message to irc server
    def sendmsg(self, channel , msg):
        print "sendmsg function"
        self.s.send("PRIVMSG "+ channel +" :"+ msg +"\n")
        print "Sending msg: ", msg

    #Function for pinging (prevent timeouts)
    def ping(self, ircmsg):
        ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
        #PING/PONG, we don't wanna time-out
        if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
            self.s.send("PONG :pingis\n")
            print "PING - PONG"

    #Function for getting messages related to the bot - ignoring the server shit
    def recvbattleshipmsg(self):
        msg = self.s.recv(2048)
        self.ping(msg)
        while("battleshipmsg:" not in msg): # wait for battleshipmsg
            msg = self.s.recv(2048)
            self.ping(msg)
        return msg


        msg = self.s.recv(2048)
        self.ping(msg)
        nick = msg.split ( '!' ) [ 0 ].replace ( ':', '' )
        message = ':'.join ( msg.split ( ':' ) [ 2: ] )
        if message.find("battleshitmsg:"):
            message = message.split(':')
            print "Found privmsg "

    def __init__(self):
        print "IrcClient _init_"
        #Making the socket
        self.s.connect(("irc.freenode.net", 6667))
        botnick = self.botnick
        channel = self.channel

        #Sending basic info to the socket
        self.s.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :I have no idea what this is for :) \n") # user authentication
        self.s.send("NICK "+ botnick +"\n") # here we actually assign the nick to the bot
        self.s.send("JOIN "+ channel +"\n") #Joins channel

#Class (thread) that listens to the server and prints out whatever it receives from the server (and prevents timeout with ping/pong)
#obsolete
class serverListener(threading.Thread):
     #CONSTRUCTAH!
    def __init__(self, ircClient):
        print "serverListener constructor"
        threading.Thread.__init__(self)
        self.ircClient = ircClient

    #Run method
    def run(self):
        while 1: # Keep doing this
             ircmsg = self.ircClient.s.recv(2048) # receive data from the server
             ircmsg = ircmsg.strip('\n\r') # removing any unnecessary linebreaks.
             print ircmsg # Here we print what's coming from the server

             #PING/PONG, we don't wanna time-out
             if ircmsg.find("PING :") != -1: # if the server pings us then we've got to respond!
                 self.ircClient.ping()
