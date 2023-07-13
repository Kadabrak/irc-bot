import random
import socket
import time
import threading
from commands.wikipedia_search import wiki
from commands.fouchan_scrap_threads import fourchan
from commands.translate_sentence import translate_sentence
from functionality.get_title import get_title
from read_file import read_file


class irc :
    
    def __init__(self,botnick,channel,server,channel_list):
        self.botnick = botnick
        self.channel = channel
        self.server = server
        self.channel_list = channel_list
        self.connexion = self.connect()
        self.socket = None

    def main(self):
        self.connect()
        self.message()
        self.socket.sendall(bytes("JOIN "+self.channel+"\n", "UTF-8"))
        time.sleep(0.3)
        for i in self.channel_list:
            self.socket.sendall(bytes("JOIN "+i+"\n", "UTF-8"))
        while 1:
            try:
                self.message()

            except KeyboardInterrupt:
                self.send()

         
    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.server,6667))
        sock.setblocking(False)
        time.sleep(0.3)
        sock.send(bytes("USER "+self.botnick +" "+self.botnick +" "+self.botnick + " " +self.botnick + "\n", "UTF-8"))
        time.sleep(0.3)
        sock.send(bytes("NICK "+self.botnick +"\n", "UTF-8"))
        time.sleep(0.3)
        sock.send(bytes("JOIN "+self.channel+"\n", "UTF-8"))
        self.socket = sock
        return sock
    
    def send(self,message,*chan):
        if chan == ():
            message_to_send = ('PRIVMSG '+self.channel+' '+':'+message)
        elif chan != ():
            message_to_send = ('PRIVMSG '+chan[0]+' '+':'+message)
        self.socket.sendall(bytes(message_to_send+"\n",encoding='utf8'))

    def ping_response(self,line):
        for i in line:
            if i.startswith('PING'):
                liste = str(i).split(' ')
                self.socket.sendall(b'PONG %b\r\n' % bytes(liste[1], 'UTF-8'))
                
    def message(self):

        try:
            data = self.socket.recv(4096)
            data = "".join(map(chr, data))
            name = data.split('!')[0][1:]
            mess = data.split(':')[2:]
            line =  data.split('\n')
            try:
                channel_message = line[0].split(' ')[2]
                if channel_message == self.botnick:
                    channel_message = name
            except:
                channel_message = None
            print(channel_message)
            message = ''
            self.ping_response(line)
            for j,i in enumerate(mess):
                if j != 0:
                    message = message+":"+i
                else:
                   message = message+i
            commande = message.strip().split(' ')
            if commande[0] == '!help':
                help_file_content = read_file('help.txt')
                for lines_help_file in help_file_content:
                    self.send(str(lines_help_file.strip()),str(name))

            elif commande[0] == '!wiki':
                wiki_url = wiki(' '.join(commande[1::]))
                self.send(wiki_url,channel_message)
                self.send(get_title(wiki_url),channel_message)
            elif commande[0] == '!join':
                self.socket.sendall(bytes("JOIN "+commande[1]+"\n", "UTF-8"))
            elif commande[0] == '!4chan':
                commande.append(None)
                if commande[1] != None:
                    list_threads = fourchan(5,commande[1])
                    for i in list_threads:
                        try:
                            title = get_title(i)
                            self.send(str(title+' => '+i),str(name))
                        except:
                            self.send(str(i),channel_message)

                else:
                    self.send(str('no chan specified'),channel_message)
            elif commande[0] == '!tr':
                self.send(translate_sentence(commande[1],commande[2],commande[3::]),channel_message)
            else:
                for i in commande:
                    if i.split(':')[0] == 'https' or i.split(':')[0] == 'http':
                        self.send(get_title(i),channel_message)
                

        except:
            pass


  


if __name__ == '__main__':
    config = read_file('config.txt')
    for i in config:
        i = i.strip().split('=')
        parameter = i[0]
        print(parameter)
        if parameter == "server":
            print(i[1])
            server = i[1]
        elif parameter == "nickname":
            nickname = i[1]
        elif parameter == "channel":
            channel = i[1].split(',')[0]
            channel_list = i[1].split(',')


    while 1:
        irc_bot = irc(nickname,channel,server,channel_list)
        try:
            irc_bot.main()
        except ConnectionResetError:
            print('The connexion was reset by the host retry in 5 seconds')
            time.sleep(5)
        except ConnectionAbortedError:
            time.sleep(5)
