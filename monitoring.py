import psutil
import platform
import logging
import re
import time

'''
class ActiveConnections:
    def __init__(self):
        self.connections = self.show_all_connections()

    def show_all_connections(self):
        connections = psutil.net_connections()
        all_connection = []
        for con in connections : 
            local_adress = f"{con.laddr.ip}:{con.laddr.port}" if con.laddr else "N/A"
            remote_adress = f"{con.raddr.ip}:{con.raddr.port}" if con.raddr else "N/A"
            status = con.status
            pid = con.pid #the process that opened the socket
            all_connection.append(f"local adress : {local_adress} | remote adress : {remote_adress} | status : {status} | PID : {pid}")
        
        return all_connection

    def show_active_connections(self):
        active_connections = []
        for con in self.connections : 
            if "ESTABLISHED" in con:
                active_connections.append(con)
        return active_connections


monitor = ActiveConnections()
all_conn = monitor.show_all_connections()
active_conn = monitor.show_active_connections()

print("All Connections:", all_conn)
print("Active Connections:", active_conn)
'''

class DetectingUnauthorizedConnections : 
    def __init__(self):
        self.os = self.detect_os()
        self.path_to_file = self.get_the_log_path()

    def detect_os(self):
        print(f"{platform.system()}")
        return platform.system()
    
    def get_the_log_path(self):
        os = self.os.lower() 
        if os == "linux":
            log_file_path = "/var/log/auth.log"
        elif os == "windows":
            log_file_path = r"C:\Windows\System32\LogFiles\SomeLogFile.log"
        elif os in ["mac","darwin"]:
            log_file_path = "/var/log/system.log"
        else:
            raise ValueError("Unsupported operating system: {}".format(os))
        
        return log_file_path

    def parse_the_log_file(self):
        logging.basicConfig(
            filename= "unauthorized_access.log",
            filemode= "a",
            format="%(asctime)s - %(levelname)s - %(message)s",
            level=logging.WARNING )
        
        ssh_fail_pattern = re.compile(r"Failed password for .* from (\d+\.\d+\.\d+\.\d+) port (\d+)")

        #TO-DO : open the file, parse the lines in which there is an error through match to the failed pattern
        try : 
            with open (self.path_to_file, "r") as log_file:
                log_file.seek(0) 
                while True :
                    line = log_file.readline()
                    if not line:
                         time.sleep(1)
                         continue
                    match = ssh_fail_pattern.search(line)
                    if match :
                        ip_adress = match.group(1)
                        port = match.group(2)
                        log_massage = f"unauthorized ssh attemp detact! IP : {ip_adress}"
                        logging.WARNING(log_massage)
        except FileNotFoundError:
            print(f"log file {self.path_to_file} not found")
        except PermissionError:
            print("premmision deny, try run the script as sudo")

detector = DetectingUnauthorizedConnections()
detector.parse_the_log_file()
