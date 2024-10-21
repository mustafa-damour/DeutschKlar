from datetime import datetime as dt
    
class Logger:
    def __init__(self, log_path:str='logs.txt'):
        self.log_path = log_path
    
    def log(self, message:str):
        f = open(self.log_path, 'a')
        f.write(message+' '+dt.now().strftime("%m/%d/%Y, %H:%M:%S.%f")+' \n')
        f.close()
        
    def get_logs(self):
        f = open(self.log_path, 'r')
        logs = f.read()
        f.close()
        return logs
    
    def get_last_n_logs(self,n:int=1):
        f = open(self.log_path, 'r')
        logs = f.read().strip()
        f.close()
        
        logs_list = logs.split('\n')
        n = min(n, len(logs_list))
        logs_list.reverse()      
        last_n_reversed =logs_list[0:n]
        last_n_reversed.reverse()
        last_n = last_n_reversed
        return '\n'.join(last_n)