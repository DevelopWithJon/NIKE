import re





class Proxyparse():
    def init(self):
        pass
    
    def authentication(self, proxy):
        find = r":"
        
        count = re.findall(find, proxy)
        
        if len(count) == 3:
            self.status = "long"
        elif len(count) == 1:
            self.status = "short"
        else:
            self.status = "bad entry"
        
        return self.status
            
    def parser(self, proxy):
        
        self.status = self.authentication(proxy)
        
        print(self.status)
        
        if self.status == "long":
            find_host = "^.*?(?=:)"
            search = re.search(find_host, proxy)
            host = search.group(0)
            print(host)  
            
            find_port = re.compile("(?<=:)\d{4,5}(?=:)")
            search = re.search(find_port, proxy)
            port = search.group(0)
            print(port)
            
            port_length = str(len(port))
            
            
            find_user = re.compile("(?<=\d{"+ port_length + "}:).*(?=:)")
            search = re.search(find_user, proxy)
            user = search.group(0)
            print(user)
            
            find_password = re.compile("(?<=:)[a-zA-Z0-9]+(?=$)")
            search = re.search(find_password, proxy)
            password = search.group(0)
            print(password)
        
        elif self.status == "short":
            find_host = "^.*?(?=:)"
            search = re.search(find_host, proxy)
            host = search.group(0)
            print(host)
            
            find_port = re.compile("(?<=:)\d{4,5}")
            search = re.search(find_port, proxy)
            port = search.group(0)
            print(port)
        
        else:
            pass
        
def main():
    Proxy