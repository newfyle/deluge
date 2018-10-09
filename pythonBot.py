
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


# In[2]:


api_link="https://api.telegram.org/"
bot_api="bot578074631:AAFcRCDPl8mzfS0AJ_zwn571cKyC4aCycZ0"


# In[3]:


def call_json(link,method,params={}):
    get_bot=requests.get(link+"/"+method,params)
    return get_bot.json()

def call_session(link,methods,params={}):
    r=requests.Session()
    r.post(link+"/"+methods,params)
    return r


# In[4]:


def countDate():
    def func(date_variable):
        func.date_var=date_variable
        return func.date_var
    func.date_var=0
    return func


# In[5]:


def unique_group_id():
    def func(group_id):
        func.g_id=group_id
        return func.g_id
    func.g_id
    return func


# In[6]:


def unique_callback():
    def func(id_cb):
        func.id=id_cb
        return func.id
    func.id=0
    return func


# In[7]:


def download(link):
    command=[api_link,"file","/",bot_api,"/",link]
    wget.download(''.join(command))


# In[8]:


class ipList:
    def __init__(self,list_ipfile):
        self.list=self.load_file(list_ipfile)
    def load_file(self,ip_file):
        data={}
        try:
            with open(ip_file,"r") as f:
                data_encrypted=f.readlines()
                for a in data_encrypted:
                    split_data=a.split("\\s")
                    data_split_decrypted={base64.b64decode(split_data[0]):base64.b64decode(split_data[1])}
                    data.update(data_split_decrypted)
            print("Data has been properly loaded.")
            return data
        except Exception as e:
            print(e)
            print("Data has not been properly loaded.")
            open(ip_file,'a').close()
            return data
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


# In[9]:


def encode_dict(dic, encoding='utf-8'):
    new_dict={}

    for key, value in dic.items():

        new_key=key.encode(encoding)

        if isinstance(value, list):
            new_dict[new_key]=[]
            for item in value:
                if isinstance(item, unicode):
                    new_dict[new_key].append(item.encode(encoding))

                elif isinstance(item, dict):

                    new_dict[new_key].append(decode_dict(item))

                else:
                    new_dict[new_key].append(item)

        elif isinstance(value, unicode):
            new_dict[new_key]=value.encode(encoding)

        elif isinstance(value, dict):
            new_dict[new_key]=decode_dict(value)

    return new_dict


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
        json_request=call_json(api_link+bot_api,"getFile",{"file_id":file_id})
        download(json_request.get('result')['file_path'])
    else:
        print("Not determined file")


# In[12]:


#figure out how to send a message in python with inlines


# In[13]:


id_group=-254621867

def send_message(text,group_id):
    params={"chat_id":str(group_id),"text":str(text)}
    json=call_json(api_link+bot_api,"sendMessage",params)
    
send_message("Rob",id_group)


# In[14]:


keyboard_button=[]

keyboard_button.append({"text":"A","url":"https://www.reddit.com/r/awwnime/"})
keyboard_button.append({"text":"Send back data","callback_data":"Avugu"})

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
    metadata = bencodepy.decode_from_file(file)
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'             + 'xt=urn:btih:' + b32hash             + '&dn=' + metadata[b'info'][b'name'].decode()             + '&tr=' + metadata[b'announce'].decode()+ '&xl=' + str(metadata[b'info'][b'length'])


# In[ ]:


date_check=countDate()
unique_cb=unique_callback()

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
                    file_id=a['message']['document']['file_id']
                    print(file_id)
                    file_name=a.get('message').get('document')['file_name']
                    torrent_buttons=[{"text":"Download","callback_data":"Download Torrent"}]
                    endswithdownload(file_id,file_name,file_ext)
                    send_message_buttons("Do you want to download torrent "+file_name+"?",a.get("message").get('chat')['id'],torrent_buttons)
                except Exception as e:
                    pprint.PrettyPrinter(indent=1).pprint(r.json())
                try:
                    query=a.get('callback_query')['id']
                    if(query!=unique_cb.id):
                        unique_cb(query)
                        query_result=a.get('callback_query')['data']
                        if(query_result=="Download Torrent"):
                            send_message("Download message received",a.get("callback_query").get("from")['id'])
                            
                    #put function here in order to call downloads
                except Exception as e:
                    print("No callback query found")
                    
                try:
                    split=a.get('message')['text'].encode("utf-8").split(" ")
                    print("Split file is "+str(split))
                    if(split[0]=="/register"):
                        username_ip_parsed=[a.get('message').get('from')['id'],split[1]]
                        class_list.delete_from_list(username_ip_parsed[0])
                        class_list.insert_to_list(username_ip_parsed)
                        send_message("If you enter an invalid ip, it may not work. You may re-register your ip on further iterations.",a.get('message').get('chat')['id'])
                        print(class_list.return_list())
                except Exception as e:
                    print(e)
                    print("No register.")
                            
                            
                        
                        
    else:
        thread.sleep(3000)

