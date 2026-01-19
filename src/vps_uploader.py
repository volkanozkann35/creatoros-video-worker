import paramiko
import os

HOST = "YOUR_VPS_IP"
USER = "root"
PASS = "YOUR_VPS_PASSWORD"

REMOTE_PATH = "/var/www/solaramade.com/videos/"


def upload_to_vps(local_file):
    filename = os.path.basename(local_file)

    ssh = paramiko.Transport((HOST, 22))
    ssh.connect(username=USER, password=PASS)
    sftp = paramiko.SFTPClient.from_transport(ssh)

    remote_file = REMOTE_PATH + filename
    sftp.put(local_file, remote_file)

    sftp.close()
    ssh.close()

    public_url = f"https://solaramade.com/videos/{filename}"
    print("🌍 VPS URL:", public_url)
    return public_url
