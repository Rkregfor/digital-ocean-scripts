import digitalocean
#from digitalocean import Action
from python_hosts import Hosts, HostsEntry
import datetime
from config import Config

manager = digitalocean.Manager(token=Config.API_TOKEN)
snapshots = manager.get_all_snapshots()
keys = manager.get_all_sshkeys()

newest_date = datetime.datetime.min

for snapshot in snapshots:
    if "gitlab" in snapshot.name.lower():
        print("[Snapshots] id = {0}, name {1}, created at {2}".format(
            snapshot.id, snapshot.name, snapshot.created_at))
        snapshot_date =  datetime.datetime.strptime(snapshot.created_at, "%Y-%m-%dT%H:%M:%SZ") 
        if snapshot_date > newest_date:
            newest_date = snapshot_date
            newest_snapshot = snapshot

print("[Snapshots] Most newest id will be used ", newest_snapshot.id, " name", newest_snapshot.name)

droplet = digitalocean.Droplet(token=Config.API_TOKEN,
                               name='GitLab-ubuntu-1gb-fra01',
                               region='fra1',    # Frankfurt
                               image=newest_snapshot.id, # 'ubuntu-16-04-x64' or snapshot id
                               #size='1024',
                               size_slug='2GB',  # 1GB
                               ssh_keys=keys,    #Automatic conversion
                               tags=["GitLab"],
                               backups=False)
print("[Droplet] Creating, id = {0}, name {1}".format(
        droplet.id, droplet.name, droplet.created_at, droplet.ip_address, droplet.status, droplet.tags))
droplet.create()

action = digitalocean.Action(id=droplet.action_ids[0], token=droplet.token, droplet_id=droplet.id)
action.load()
action.wait()

droplet = manager.get_droplet(droplet.id)

print("[Droplet] Created, id = {0}, name {1}, created at {2}, ip {3}, status {4}, tags = {5}".format(
        droplet.id, droplet.name, droplet.created_at, droplet.ip_address, droplet.status, droplet.tags))
print("[Complete] Gitlab create from snapshot")


hosts = Hosts(path='/etc/hosts')
if hosts.exists(names=Config.NAMES):
    hosts.remove_all_matching(name=Config.NAMES[0])
    new_entry = HostsEntry(entry_type='ipv4', address=droplet.ip_address, names=Config.NAMES)
    hosts.add([new_entry])
    hosts.write()