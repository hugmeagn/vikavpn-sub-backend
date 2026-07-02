import json
import subprocess
from pathlib import Path

from ..users import get_or_create_uid


def setup_xray(credentials, xray_privkey):
    Path('data').mkdir(parents=True, exist_ok=True)

    uuids = [get_or_create_uid(username) for username in credentials.keys()]
    clients = [{"id": uuid} for uuid in uuids]
    clients_with_flow = [{"id": uuid, "flow": "xtls-rprx-vision"} for uuid in uuids]

    with open("templates/xray.json") as f:
        config = json.load(f)

    for inbound in config["inbounds"]:
        if inbound["streamSettings"]["network"] == "tcp":
            inbound["settings"]["clients"] = clients_with_flow
            inbound["streamSettings"]["realitySettings"]["privateKey"] = xray_privkey
        else:
            inbound["settings"]["clients"] = clients

    with open("/usr/local/etc/xray/config.json", "w") as f:
        json.dump(config, f, indent=2)

    subprocess.run(["systemctl", "restart", "xray"])
