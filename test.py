from functionality.message_box.msg import get_msg,place_msg

place_msg('lolpop','dth',['salut'])
for i in get_msg("dth"):
    print(i.strip())
