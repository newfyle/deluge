
# coding: utf-8

# In[1]:


import requests
import wget
import base64
import time
import pprint
import json, ast
import delugeBot
import os
import socket
from IPy import IP
import sys
from OpenSSL import SSL, crypto
import bcoding, hashlib,urllib
import io
from delugeBot import DelugeConnect as deluge_connect
from Crypto.Cipher import AES
import base64


# In[2]:


api_link="https://api.telegram.org/"
bot_api=""
with open("botapi.txt","r") as f:
    b=f.read()
    obj2=AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
    bot_api=obj2.decrypt(b)


# In[3]:


for a in os.listdir("."):
    if a.endswith(".torrent"):
        os.remove(a)


# In[4]:


def call_json(link,method,params={}):
    get_bot=requests.get(link+"/"+method,params)
    return get_bot.json()

def call_session(link,methods,params={}):
    r=requests.Session()
    r.post(link+"/"+methods,params)
    return r


# In[18]:


def countDate():
    def func(date_variable):
        func.date_var=date_variable
        with open("id_var.txt","w") as f:
            f.write(str(date_variable))
        return func.date_var
    func.date_var=0
    return func


# In[19]:


def unique_group_id():
    def func(group_id):
        func.g_id=group_id
        return func.g_id
    func.g_id
    return func


# In[20]:


def unique_callback():
    def func(id_cb):
        func.id=id_cb
        with open("idcb_var.txt","w") as f:
            f.write(str(id_cb))
        return func.id
    func.id=0
    return func


# In[8]:


def download(link):
    command=[api_link,"file","/",bot_api,"/",link]
    wget.download(''.join(command))


# In[9]:


class ipList:
    def __init__(self,list_ipfile):
        self.list=self.load_file(list_ipfile)
    def load_file(self,ip_file):
        data_lists={}
        try:
            with open(ip_file,"r") as f:
                data_encrypted=f.readlines()
                for a in data_encrypted:
                    split_data=a.split("\\s")
                    data_split_decrypted={base64.b64decode(split_data[0]):base64.b64decode(split_data[1])}
                    data_lists.update(data_split_decrypted)
            print("Data has been properly loaded.")
            return data_lists
        except Exception as e:
            print(e)
            print("Data has not been properly loaded.")
            open(ip_file,'a').close()
            return data_lists
    def save_file(self,ip_file):
        if(os.path.exists(ip_file)):
            os.remove(ip_file)
            print("File has been deleted for new save.")
        else:
            print("File does not exist, proceed with saving.")
        with open(ip_file,"w") as f:
            try:
                for a in self.list.items():
                    string_save_encoded=base64.b64encode(a[0])+"  "+base64.b64encode(a[1])
                    f.write(string_save_encoded)
            except Exception as e:
                print("Data list is empty")
    def insert_to_list(self,username_ip):
        if(username_ip[0] not in self.list):
            self.list.update({username_ip[0]:username_ip[1]})
        print(username_ip)
    def delete_from_list(self,username):
        try:
            del self.list[username]
            print(username+" deleted")
        except Exception as e:
            print("No user id listed")
    def return_ip(self,username):
        return self.list.get(username)
    def return_list(self):
        return self.list
    def clear_file(self,ip_file):
        if(os.path.exists(ip_file)):
            os.remove(ip_file)
        self.list={}

class_list=ipList("saved_user_lists")
class_list.load_file("saved_user_lists")


# In[10]:


def request_getter():
    def func(offset):
        func.r=requests.get(api_link+bot_api+"/"+"getUpdates",{"offset":str(offset),"timeout":"3"})
        return func.r
    func.r=requests.get(api_link+bot_api+"/"+"getUpdates",{"offset":"1","timeout":"3"})
    return func


# In[11]:


def endswithdownload(file_id,name_file,array_of_item):
    print(name_file.split(".")[-1])
    if(name_file.split(".")[-1] in array_of_item):
        print("Attempt downloading")
        json_request=call_json(api_link+bot_api,"getFile",{"file_id":file_id})
        file_name=json_request.get('result')['file_path']
        download(file_name)
        os.rename(file_name.split("/")[-1],name_file)
    else:
        print("Not determined file")


# In[12]:


#figure out how to send a message in python with inlines


# In[13]:


def send_message(text,group_id):
    params={"chat_id":str(group_id),"text":str(text)}
    json=call_json(api_link+bot_api,"sendMessage",params)


# In[14]:


def send_message_buttons(text,group_id,query_buttons):
    object=json.dumps({"inline_keyboard":[query_buttons]})
    params={"chat_id":str(group_id),"text":str(text),"reply_markup":object}
    jsona=call_json(api_link+bot_api,"sendMessage",params)
    print(jsona)


# In[15]:


def download_torrent(file_name,group_id_download):
    keyboard_buttons=[{"text":"Download Torrent","callback_data":"Start Torrent Download"}]
    send_message_buttons("Do you want to download torrent "+file_name+" ?",group_id_download,json.dumps({"inline_keyboard":[keyboard_buttons]}))
    returned_get_result=call_json(api_link+bot_api,"sendMessage",params)


# In[16]:


def make_magnet_from_file(file) :
    file_torrent=open(file,"rb")
    metadata = bcoding.bdecode(file_torrent.read())
    subj = metadata[b'info']
    hashcontents = bcoding.bencode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'+ 'xt=urn:btih:' + b32hash+ '&dn=' + metadata[b'info'][b'name'].decode()+ '&tr=' + metadata[b'announce'].decode()+ '&xl=' + str(metadata[b'info'][b'length'])


# In[ ]:


date_check=countDate()
unique_cb=unique_callback()

try:
    saved_id = open('id_var.txt', 'r')
    line_first = int(saved_id.readline())

    date_check(line_first)
    
except Exception as e:
    print(e)
    print("Something is wrong with the save of unique chat id. Blank slate is loaded.")
    
try:
    saved_cb=open('idcb_var.txt','r')
    line_first_cb=int(saved_cb.readline())

    
    unique_cb(line_first_cb)
except Exception as e:
    print(e)
    print("Something wrong with cb unique.Blank slate.")

while True:
    raw=request_getter()
    r=raw.r
    if(r.status_code==200):
        
        for a in r.json()[u'result']:
            if(int(a['update_id'])>int(date_check.date_var)):
                pprint.PrettyPrinter(indent=1).pprint(a.get('message'))
                date_check(int(a['update_id']))
                raw(str(a['update_id']))
                try:
                    file_ext=['torrent']
                    file_id=a.get('message').get('document')['file_id']
                    print(file_id)
                    file_name=a.get('message').get('document')['file_name']
                    print(file_name)
                    torrent_buttons=[{"text":"Download","callback_data":"Download Torrent"}]
                    endswithdownload(file_id,file_name,file_ext)
                    send_message_buttons("Do you want to download torrent "+file_name+" ?",a.get("message").get('chat')['id'],torrent_buttons)
                except Exception as e:
                    print("Something failed on the detection or download of torrent")
                    print(e)
                    print("End")
                    pprint.PrettyPrinter(indent=1).pprint(r.json())
                    
                try:
                    query=a.get('callback_query')['id']
                    if(query!=unique_cb.id):
                        pprint.PrettyPrinter(indent=1).pprint(a.get('callback_query'))
                        unique_cb(query)
                        query_result=a.get('callback_query')['data']
                        query_from=a.get('callback_query').get('from')['id']
                        if(query_result=="Download Torrent"):
                            stringTorrents=a.get('callback_query').get('message')['text'].split(" ")
                            new_client=deluge_connect(class_list.return_ip(query_from),58846,"localclient","a")
                            print(new_client.disconnect())
                            print(new_client.connect())
                            print(stringTorrents[-2])
                            new_client.add_torrent(stringTorrents[-2])
                            new_client.disconnect()
                            #ut function here in order to call downloads
                except Exception as e:
                    print(str(e)+" is error of deluge")
                    print("No callback query found")
                    
                try:
                    split=a.get('message')['text'].encode("utf-8").split()
                    print("Split file is "+str(split))
                    if(split[0]=="/register"):
                        if(split[1]=='127.0.0.1' or split[1]=='localhost'):
                            send_message("Reference to local apis are banned, period.",a.get('message').get('chat')['id'])
                        else:
                            username_ip_parsed=[a.get('message').get('from')['id'],split[1]]
                            print(str(username_ip_parsed)+" is ip")
                            class_list.delete_from_list(username_ip_parsed[0])
                            class_list.insert_to_list(username_ip_parsed)
                            class_list.save_file("saved_user_lists")
                            send_message("If you enter an invalid ip, it may not work. You may re-register your ip on further iterations.",a.get('message').get('chat')['id'])
                            print(class_list.return_list())
                    elif(split[0]=="/status"):
                        print(str(username_ip_parsed)+" is ip")
                        chat_id=a.get('message').get('chat')['id']
                        print(chat_id)
                        status_client=deluge_connect(class_list.return_ip(a.get('message').get('from')['id']),58846,"localclient","a")
                        status_client.disconnect()
                        status_client.connect()
                        list_of_progress=status_client.get_torrent_status()
                        print(list_of_progress)
                        string_prepared=[]
                        for a in list_of_progress:
                            string_prepared.append(str(a['name']+" progress is at "+str(int(a['progress']))+"%"))
                        print(string_prepared)
                        send_message(("\n".join(string_prepared)),chat_id)
                except Exception as e:
                    print(e)
                    print("No register.")
                            
                            
                        
                        
    else:
        thread.sleep(3000)

