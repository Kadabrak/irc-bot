import random
import socket
import time
import threading
from commands.wikipedia_search import wiki
from commands.fouchan_scrap_threads import fourchan
from commands.translate_sentence import translate_sentence
import requests
import bs4


class irc :
    
    def __init__(self):
        self.botnick = 'qsdiop'
        self.channel = '#PSYclantest'
        self.server = 'alterland.net'
        self.connexion = self.connect()
        self.socket = None

    def main(self):
        self.connect()
        while 1:
            self.socket.sendall(bytes("JOIN "+self.channel+"\n", "UTF-8"))
            data = self.socket.recv(4096)
            data = "".join(map(chr, data))
            try:
                self.commands(data)
            except:
                self.message(data)

            

         
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

    def get_title(self,url):
        r = requests.get(url)
        html = bs4.BeautifulSoup(r.text,'html.parser')
        html = str(html.title)[7:-8]
        message = '.:['+html+']:.'
        return message

    def message(self,data):
        line =  data.split('\n')
        for i in line:
            if i.startswith('PING'):
                liste = str(i).split(' ')
                self.socket.sendall(b'PONG %b\r\n' % bytes(liste[1], 'UTF-8'))
            else:
                self.commands(data)
        return data

    def commands(self,data):
        name = data.split('!')[0][1:]
        mess = data.split(':')[2:]
        message = ''
        for j,i in enumerate(mess):
            if j != 0:
                message = message+":"+i

            else:
                message = message+i
                    #irc.affichage(self,name+' > '+message)
            commande = message.strip().split(' ')

            if commande[0] == '!help':
                help_respond = ['this bot display the title of a web page create by lolpop you can found me on #PSYclan','commands available:','- !wiki [word] to get the wikipedia of the word',"- !4chan [board] to get the fivest hot threads","don't forget 'Si vis pacem para bellum (ty Charlotte)'","and this is my favorite song: https://www.youtube.com/watch?v=FuSsi-LubGU"]
                for text in help_respond:
                    self.send(str(text),str(name))

            elif commande[0] == '!wiki':
                    wiki_url = wiki(commande[1])
                    self.send(wiki_url)
                    self.send(self.get_title(wiki_url))
                        

            elif commande[0] == '!4chan':
                commande.append(None)
                print(commande[0])
                if commande[1] != None:
                    list_threads = fourchan(5,commande[1])
                    for i in list_threads:
                        try:
                            title = self.get_title(i)
                            self.send(str(title+' => '+i),str(name))
                        except:
                            self.send(str(i))

                    else:
                        self.send(str('no chan specified'))
            elif commande[0] == '!tr':
                print(commande[1],commande[2],' '.join(commande[3::]))
                print(translate_sentence(commande[1],commande[2],commande[2::]))
                self.send(translate_sentence(commande[1],commande[2],commande[3::]))
            else:
                for i in mess:
                    if i.split(':')[0] == 'https' or i.split(':')[0] == 'http':
                        self.send(self.get_title(i))
                

if __name__ == '__main__':
    while 1:
        try:
            serveur = irc()
            serveur.main()
        except ConnectionAbortedError:
            time.sleep(1)
