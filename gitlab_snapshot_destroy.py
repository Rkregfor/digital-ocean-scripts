import digitalocean
import datetime
from config import Config

manager = digitalocean.Manager(token=Config.API_TOKEN)
droplets = manager.get_all_droplets()

for droplet in droplets:
    print("[Droplet] id = {0}, name {1}, created at {2}, ip {3}, status {4}, tags = {5}".format(
        droplet.id, droplet.name, droplet.created_at, droplet.ip_address, droplet.status, droplet.tags))
    if 'GitLab'in droplet.tags:
        name = "Snapshot_{0}_{1}".format(datetime.datetime.utcnow(), droplet.name)
        
        print("[Snapshot] Started for {0}".format(droplet))
        action = droplet.take_snapshot(name, return_dict=False, power_off=True)
        action.wait()
        print("[Snapshot] Created '{0}' for {1}".format(name, droplet))
  
        confirmed = input("Are you sure you want to destroy droptlet? Type yes/no")
        if len(confirmed) > 0 and confirmed.lower() == 'yes':
            droplet.destroy()
             print("[Droplet] Destroyed id = {0}, name {1}", droplet.id, droplet.name)

print("[Complete] Gitlab backup and destory")