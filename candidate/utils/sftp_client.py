# my_app/utils/sftp_client.py

import paramiko

class SFTPClient:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.client = None
        self.sftp = None

    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(self.hostname, port=self.port, username=self.username, password=self.password)
        self.sftp = self.client.open_sftp()

    def list_dir(self, path):
        return self.sftp.listdir_attr(path)

    def get_file(self, remote_path, local_path):
        self.sftp.get(remote_path, local_path)

    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
