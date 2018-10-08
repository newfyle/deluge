
# coding: utf-8

# In[8]:


import requests
import wget
import base64
import time
import pprint
import json
import delugeBot


# In[9]:


api_link="https://api.telegram.org/"
bot_api="bot578074631:AAFcRCDPl8mzfS0AJ_zwn571cKyC4aCycZ0"


# In[10]:


def call_json(link,method,params={}):
    get_bot=requests.get(link+"/"+method,params)
    return get_bot.json()

def call_session(link,methods,params={}):
    r=requests.Session()
    r.post(link+"/"+methods,params)
    return r


# In[11]:


def countDate():
    def func(date_variable):
        func.date_var=date_variable
        return func.date_var
    func.date_var=0
    return func


# In[12]:


def unique_callback():
    def func(id_cb):
        func.id=id_cb
        return func.id
    func.id=0
    return func


# In[13]:


def download(link):
    command=[api_link,"file","/",bot_api,"/",link]
    wget.download(''.join(command))


# In[14]:


def request_getter():
    def func(offset):
        func.r=requests.get(api_link+bot_api+"/"+"getUpdates",{"offset":str(offset),"timeout":"3"})
        return func.r
    func.r=requests.get(api_link+bot_api+"/"+"getUpdates",{"offset":"1","timeout":"3"})
    return func


# In[21]:


date_check=countDate()
unique_cb=unique_callback()

while True:
    raw=request_getter()
    r=raw.r
    if(r.status_code==200):
        #pprint.PrettyPrinter(indent=3).pprint(r.json())
        for a in r.json()['result']:
            if(a['update_id']>date_check.date_var):
                pprint.PrettyPrinter(indent=1).pprint(a.get('message'))
                date_check(a['update_id'])
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
                    pprint.PrettyPrinter(indent=1).pprint(r.json())
    else:
        thread.sleep(3000)


# In[15]:


def endswithdownload(file_id,name_file,array_of_item):
    print(name_file.split(".")[-1])
    if(name_file.split(".")[-1] in array_of_item):
        json_request=call_json(api_link+bot_api,"getFile",{"file_id":file_id})
        download(json_request.get('result')['file_path'])
    else:
        print("Not determined file")


# In[16]:


#figure out how to send a message in python with inlines


# In[17]:


id_group=-254621867

def send_message(text,group_id):
    params={"chat_id":str(group_id),"text":str(text)}
    json=call_json(api_link+bot_api,"sendMessage",params)
    
send_message("Rob",id_group)


# In[18]:


keyboard_button=[]

keyboard_button.append({"text":"A","url":"https://www.reddit.com/r/awwnime/"})
keyboard_button.append({"text":"Send back data","callback_data":"Avugu"})

def send_message_buttons(text,group_id,query_buttons):
    object=json.dumps({"inline_keyboard":[query_buttons]})
    params={"chat_id":str(group_id),"text":str(text),"reply_markup":object}
    jsona=call_json(api_link+bot_api,"sendMessage",params)
    print(jsona)


# In[19]:


def download_torrent(file_name,group_id_download):
    keyboard_buttons=[{"text":"Download Torrent","callback_data":"Start Torrent Download"}]
    send_message_buttons("Do you want to download torrent "+file_name+" ?",group_id_download,json.dumps({"inline_keyboard":[keyboard_buttons]}))
    returned_get_result=call_json(api_link+bot_api,"sendMessage",params)


# In[ ]:


def make_magnet_from_file(file) :
    metadata = bencodepy.decode_from_file(file)
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'             + 'xt=urn:btih:' + b32hash             + '&dn=' + metadata[b'info'][b'name'].decode()             + '&tr=' + metadata[b'announce'].decode()+ '&xl=' + str(metadata[b'info'][b'length'])

