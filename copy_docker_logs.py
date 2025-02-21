import paramiko
import datetime
import getpass
import argparse
import traceback
from scp import SCPClient


class SSHClientManager:
    """Handles SSH connection and command execution."""

    def __init__(self, host, username, password):
        self.host = host
        self.username = username
        self.password = password
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.connect()

    def connect(self):
        """Establish SSH connection."""
        try:
            self.client.connect(hostname=self.host, username=self.username, password=self.password)
            print(f"Connected to {self.host}")
        except Exception as e:
            print(f"SSH connection failed: {str(e)}")
            traceback.print_exc()
            exit(1)

    def execute_command(self, command):
        """Execute a command over SSH."""
        try:
            stdin, stdout, stderr = self.client.exec_command(command)
            error_output = stderr.read().decode()
            if error_output:
                print(f"Error executing command: {error_output}")
                return None
            return stdout.read().decode()
        except Exception as e:
            print(f"Error executing SSH command: {str(e)}")
            traceback.print_exc()
            return None

    def close(self):
        """Close the SSH connection."""
        self.client.close()
        print("SSH connection closed.")


class DockerLogExtractor:
    """Handles Docker log extraction via SSH."""

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def extract_logs(self, docker_name, since_time, until_time):
        """Extract logs from the specified Docker container."""
        current_date = datetime.datetime.now().strftime("%m%d")
        log_file_name = f"{docker_name}{current_date}.log"
        remote_file_path = f"/tmp/{log_file_name}"

        command = f"docker logs --since {since_time} --until {until_time} current-{docker_name}-1 2>&1 > {remote_file_path}"
        output = self.ssh_client.execute_command(command)

        if output is not None:
            print(f"Logs saved to {remote_file_path} on the remote machine.")
            return remote_file_path
        return None


class LogFileTransfer:
    """Handles file transfer via SCP."""

    def __init__(self, ssh_client):
        self.ssh_client = ssh_client

    def copy_logs_to_local(self, remote_file_path, local_directory):
        """Copy extracted logs from remote to local machine."""
        try:
            local_file_path = f"{local_directory}/{remote_file_path.split('/')[-1]}"
            with SCPClient(self.ssh_client.client.get_transport()) as scp:
                scp.get(remote_file_path, local_file_path)
                print(f"Logs copied to local machine: {local_file_path}")
        except Exception as e:
            print(f"Error during SCP transfer: {str(e)}")
            traceback.print_exc()


class LogExtractorManager:
    """Orchestrates the log extraction and file transfer process."""

    def __init__(self, host, username, password, local_directory):
        self.ssh_client = SSHClientManager(host, username, password)
        self.docker_log_extractor = DockerLogExtractor(self.ssh_client)
        self.file_transfer = LogFileTransfer(self.ssh_client)
        self.local_directory = local_directory

    def extract_and_transfer_logs(self, docker_names, since_time, until_time):
        """Extract logs from multiple containers and transfer them."""
        for docker in docker_names:
            remote_path = self.docker_log_extractor.extract_logs(docker, since_time, until_time)
            if remote_path:
                self.file_transfer.copy_logs_to_local(remote_path, self.local_directory)

    def close(self):
        """Close SSH connection."""
        self.ssh_client.close()


def main():
    """Parse arguments and initiate log extraction."""
    parser = argparse.ArgumentParser(description="Extract Docker logs via SSH")
    parser.add_argument("--host", required=True, help="The target host IP address")
    parser.add_argument("--dockers", required=True, nargs="+", help="List of Docker containers")
    parser.add_argument("--since", required=True, help="Start time (YYYY-MM-DDTHH:MM:SS)")
    parser.add_argument("--until", required=True, help="End time (YYYY-MM-DDTHH:MM:SS)")
    parser.add_argument("--local_dir", default="/mnt/c/Users/guy/Desktop", help="Local directory to save logs")

    args = parser.parse_args()
    username = "bndc"
    password = getpass.getpass("Enter the password: ").strip()

    manager = LogExtractorManager(args.host, username, password, args.local_dir)
    manager.extract_and_transfer_logs(args.dockers, args.since, args.until)
    manager.close()


if __name__ == "__main__":
    main()
