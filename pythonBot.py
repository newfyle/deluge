
# coding: utf-8

# In[12]:


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


# In[58]:


api_link="https://api.telegram.org/"
bot_api=""
with open("botapi.txt","r") as f:
    b=f.read()
    obj2=AES.new('This is a key123', AES.MODE_CFB, 'This is an IV456')
    bot_api=obj2.decrypt(b)
print(bot_api)


# In[49]:


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


# In[14]:


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


# In[34]:


def make_magnet_from_file(file) :
    file_torrent=open(file,"rb")
    metadata = bcoding.bdecode(file_torrent.read())
    subj = metadata[b'info']
    hashcontents = bcoding.bencode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'+ 'xt=urn:btih:' + b32hash+ '&dn=' + metadata[b'info'][b'name'].decode()+ '&tr=' + metadata[b'announce'].decode()+ '&xl=' + str(metadata[b'info'][b'length'])
    '''torrent = open(file, 'r').read()
    metadata = bcoding.bdecode(torrent)
    hashcontents = bcoding.bencode(metadata['info'])
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest)
    params = {'xt': 'urn:btih:%s' % b32hash,\
              'dn': metadata['info']['name'],\
              'tr': metadata['announce'],\
              'xl': metadata['info']['length']}
    paramstr = urllib.urlencode(params)
    magneturi = 'magnet:?%s' % paramstr
    return magneturi'''


# In[35]:


def verify_cb(conn, cert, errnum, depth, ok):
    certsubject = crypto.X509Name(cert.get_subject())
    commonname = certsubject.commonName
    print('Got certificate: ' + commonname)
    return ok


# In[48]:


date_check=countDate()
unique_cb=unique_callback()
client_send_download_commands=ClientSSL(os.curdir,'client.pkey','client.cert','CA.cert')

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
                    send_message_buttons("Do you want to download torrent "+file_name+" ?",a.get("message").get('chat')['id'],torrent_buttons)
                except Exception as e:
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
                            print(stringTorrents)
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


# In[45]:


class ClientSSL:
    def __init__(self,dir_self,client_key,client_cert,ca_cert):
        self.dir=self.set_dir(dir_self)
        self.ctx=SSL.Context(SSL.SSLv23_METHOD)
        self.ctx.set_options(SSL.OP_NO_SSLv2)
        self.ctx.set_options(SSL.OP_NO_SSLv3)
        self.ctx.set_verify(SSL.VERIFY_PEER, verify_cb)  # Demand a certificate
        #self.ctx.use_privatekey_file(os.path.join(dir, 'client.pkey'))
        #self.ctx.use_certificate_file(os.path.join(dir, 'client.cert'))
        #self.ctx.load_verify_locations(os.path.join(dir, 'CA.cert'))
        self.ctx.use_privatekey_file(os.path.join(self.dir, client_key))
        self.ctx.use_certificate_file(os.path.join(self.dir,client_cert))
        self.ctx.load_verify_locations(os.path.join(self.dir,ca_cert))
        self.sock = SSL.Connection(self.ctx, socket.socket(socket.AF_INET, socket.SOCK_STREAM))
    def send(self,host,port,message):
        #ensure this part in later stages that 127.0.0.1 or localhost must be banned
        self.sock.connect(host,port)
        """while 1:
            line = sys.stdin.readline()
            if line == '':
                break
            try:
                self.sock.send(line)
                sys.stdout.write(sock.recv(1024).decode('utf-8'))
                sys.stdout.flush()
            except SSL.Error:
                print('Connection died unexpectedly')
                break
        self.sock.shutdown()
        self.sock.close()"""
        count=0
        while (count!=5):
            try:
                self.sock.send(message)
                sys.stdout.write(sock.recv(1024).decode('utf-8'))
                sys.stdout.flush()
                break
            except SSL.Error:
                print('Connection died unexpectedly, retrying')
                count+=1
                continue
        self.sock.shutdown()
        self.sock.close()
    def set_dir(self,dir):
        return dir

