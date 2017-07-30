import digitalocean
#from digitalocean import Action
from python_hosts import Hosts, HostsEntry
import datetime
from config import Config

manager = digitalocean.Manager(token=Config.API_TOKEN)
snapshots = manager.get_all_snapshots()
keys = manager.get_all_sshkeys()

droplets = manager.get_all_droplets(tag_name='GitLab')

for droplet in droplets:
    print("[Droplet] Found by tag, id = {0}, name {1}, created at {2}, ip {3}, status {4}, tags = {5}".format(
        droplet.id, droplet.name, droplet.created_at, droplet.ip_address, droplet.status, droplet.tags))

hosts = Hosts(path='/etc/hosts')
if hosts.exists(names=Config.NAMES):
    hosts.remove_all_matching(name='build.wordexter.com')

new_entry = HostsEntry(entry_type='ipv4', address=droplet.ip_address, names=Config.NAMES)
hosts.add([new_entry])
hosts.write()

print("[Complete] Gitlab update hosts file by droplet's ip")