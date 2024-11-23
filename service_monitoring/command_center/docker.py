import paramiko
import json
import requests

def retrieve_docker_info(host, username, key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        private_key = paramiko.RSAKey.from_private_key_file(key_path)
        
        # Connect to the remote server
        ssh.connect(hostname=host, username=username, pkey=private_key)
        command = 'docker ps -a --format "{{.Names}} {{.Image}}"'
    
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()
        
        if errors:
            print(f"Errors on {host}: {errors}")
        else:
            # Split and parse individual JSON entries
            containers = [json.loads(line) for line in output.splitlines()]
            return containers

    except Exception as e:
        print(f"Error connecting to {host}: {e}")
    finally:
        ssh.close()

# retrieve server list with server name, username and path from rest api db
def get_servers_from_api(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve servers: {response.status_code}")
        return []

api_url = "http://example.com/api/servers"
hosts = get_servers_from_api(api_url)

for host in hosts:
    print(f"Details for {host['host']}: {retrieve_docker_info(host['host'], host['username'], host['password'])}")