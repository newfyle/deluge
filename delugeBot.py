
# coding: utf-8

# In[58]:


from deluge_client import DelugeRPCClient,FailedToReconnectException
import base64
import pprint


# In[59]:


printp=pprint.PrettyPrinter(indent=1)


# In[89]:


class DelugeConnect:
    def __init__(self,host,port,username,password):
        self.host=host
        self.port=port
        self.username=username
        self.password=password
        
    def connect(self):
        self.client = DelugeRPCClient(self.host, self.port, self.username, self.password, automatic_reconnect=True)
        #please recommend everyone else to make a proper client username and password
        try:
            self.client.connect()
            return "Client connected."
        except Exception as e:
            print(e)
            return "Cannot connect, something is wrong."
        
    def add_torrent(self,filename):
        torrent=open(filename,'r').read()
        print(torrent)
        metadata = base64.b64encode(torrent)
        #self.call_retry(self.client,'core.add_torrent_file',filename,metadata,{})
        return self.client.core.add_torrent_file(filename,metadata,{})
                
    def get_torrent_status(self):
        raw_progress=self.client.core.get_torrents_status({}, ['name','progress'])
        list_of_progress=[]
        for a in raw_progress.items():
            list_of_progress.append(a[1])
        return list_of_progress
            
    def disconnect(self):
        try:
            self.client.disconnect()
            return "Disconnected"
        except Exception as e:
            print(e)
            return "Cannot be disconnected, maybe it's already disconnected?"
    


# In[ ]:


"""for a in client_connect.get_torrent_status().items():
    print(type(a))
    printp.pprint(a[1]['name']+" "+str(a[1]['progress']))
    print("break")"""

