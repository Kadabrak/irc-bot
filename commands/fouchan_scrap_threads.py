import urllib.request
def fourchan(nbr_threads,chan=None):
    try:
        message = []
        nbr_threads = int(nbr_threads)
        site= "https://boards.4channel.org/"
        site = site+chan+'/'
        hdr = {'User-Agent':'Mozilla/5.0'}
        req = urllib.request.Request(site,headers=hdr)
        html = urllib.request.urlopen(req).readlines()
        for ligne in html:
            spliter = ligne.decode('utf-8').split('"')
            for i,page in enumerate(spliter):
                if len(message) < nbr_threads:
                    if page == "Reply to this post":
                        if spliter[i+2] == 'postInfo desktop':
                            pass
                        elif spliter[i+2] == 'file':
                            pass
                        
                        elif spliter[i+2] == 'postMessage':
                            pass
                        elif spliter[i+2] == '//s.4cdn.org/image/sticky.gif':
                            pass
                        else:
                            message.append(site+spliter[i+2])
            return message
    except:
        return ["I can't get this board",]



