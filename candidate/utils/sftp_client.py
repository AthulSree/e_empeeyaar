# my_app/utils/sftp_client.py

import paramiko
import zipfile
import os
import io
import stat

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

    def compress_dir(self, remote_path):
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            self._compress_dir(remote_path, '', zipf)
        buffer.seek(0)
        return buffer

    def _compress_dir(self, remote_path, base_path, zipf):
        for item in self.sftp.listdir_attr(remote_path):
            item_path = os.path.join(remote_path, item.filename)
            arcname = os.path.join(base_path, item.filename)
            if stat.S_ISDIR(item.st_mode):
                self._compress_dir(item_path, arcname, zipf)
            else:
                with self.sftp.file(item_path, 'rb') as file:
                    zipf.writestr(arcname, file.read())




    def disconnect(self):
        if self.sftp:
            self.sftp.close()
        if self.client:
            self.client.close()
