import json

def retrieve_docker_info(host, username, ssh, private_key):
    try:
        ssh.connect(hostname=host, username=username, pkey=private_key)
        command = 'docker ps -a --format "{{.Names}} {{.Image}}"'
    
        stdin, stdout, stderr = ssh.exec_command(command)
        output = stdout.read().decode().strip()
        errors = stderr.read().decode().strip()
        
        if errors:
            print(f"Errors on {host}: {errors}")
        else:
            metrics = [json.loads(line) for line in output.splitlines()]
            return metrics

    except Exception as e:
        print(f"Error connecting to {host}: {e}")
    finally:
        ssh.close()