import docker
from pprint import pprint

client = docker.DockerClient(base_url="unix:///var/run/docker.sock")
for container in client.containers.list():
    # pprint(container.stats(decode=None, stream=False))
    print(container.stats(decode=None, stream=False).keys())
