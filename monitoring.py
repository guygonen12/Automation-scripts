import psutil

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

'''
monitor = ActiveConnections()
all_conn = monitor.show_all_connections()
active_conn = monitor.show_active_connections()

print("All Connections:", all_conn)
print("Active Connections:", active_conn)
'''


