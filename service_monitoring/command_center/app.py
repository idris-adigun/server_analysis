import requests
import paramiko
import docker_metric as docker_metric


def main(server, username, key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        data = docker_metric.retrieve_docker_info(server, username, ssh, private_key)
        return data
    except Exception as e:
        print(f"{e}")
    
    
# def get_servers_from_api(api_url):
#     response = requests.get(api_url)
#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Failed to retrieve servers: {response.status_code}")
#         return []

if __name__ == "__main__":
        print(main("127.0.0.1", "idris", '/home/idris/.ssh/id_rsa'))
        # print(main("127.0.0.1", "root", '/root/.ssh/id_ed25519.pub'))