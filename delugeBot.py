
# coding: utf-8

# In[8]:


from deluge_client import DelugeRPCClient,FailedToReconnectException


# In[97]:


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
        metadata = base64.b64encode(torrent)
        self.call_retry(self.client,'core.add_torrent_file','archlinux.torrent',metadata,{})
        
    def call_retry(self, method, *args, **kwargs):
        for a in range(10):
            try:
                print("Adding")
                return self.client.call(method, *args, **kwargs)
            except FailedToReconnectException:
                print("Fail to add")
                time.sleep(5)
                
    def get_torrent_status(self):
        return call_retry(self.client, 'core.get_torrents_status', {}, [])
    
    def add_torrent_magnet(self,magnet_link):
        try:
            return call_retry(self.client,'core.add_torrent_magnet',magnet_link,{})
        except Exception as e:
            add_torrent_error="<class \'deluge_client.client.AddTorrentError\'>"
            type_check=str(type(e))
            if(type_check==add_torrent_error):
                return "Torrent already exists in the machine"
            
    def disconnect(self):
        try:
            self.client.disconnect()
            return "Disconnected"
        except Exception as e:
            print(e)
            return "Cannot be disconnected, maybe it's already disconnected?"


# In[98]:


new_self=DelugeConnect('127.0.0.1',58846,'localclient','a')


# In[99]:


new_self.connect()

