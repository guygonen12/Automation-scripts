import psutil

class active_connections:
    def __init__(self):
        self.connections = show_all_connections()

    def show_all_connections():
        connections = psutil.net_connections()
        all_connection = []
        for con in connections : 
            local_adress = f"{con.laddr.ip}:{con.laddr.port}" if con.laddr else "N/A"
            remote_adress = f"{con.raddr.ip}:{con.raddr.ip}" if con.raddr else "N/A"
            status = con.status
            pid = con.pid #the process that opened the socket
            all_connection.append(f"local adress : {local_adress} | remote adress : {remote_adress} | status : {status} | PID : {pid}")
