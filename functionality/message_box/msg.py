import os

def get_msg(name_reciver):
    path = os.getcwd()
    box_path = path+'/functionality/message_box'
    file_in_path = os.listdir(box_path)
    for i in file_in_path:
        if i[0:-4] == name_reciver:
            fich_message = box_path+'/'+i
            with open(fich_message,'r') as fich:
                fich_content = fich.readlines()
            os.remove(fich_message)
            return fich_content
    else:
        return False

def place_msg(sender,reciver,message):
    path = os.getcwd()
    box_path = path+'/functionality/message_box'
    try:
        with open((box_path+'/'+reciver+'.txt'),'a') as fich:
            fich.write(('from '+ sender +' ' + ' '.join(message) +'\n'))
            return True
    except:
        return False
