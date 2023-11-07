import os
import json
import logging
import sys

from ping3 import ping
from datetime import datetime
from rich.console import Console
from rich.logging import RichHandler

console = Console()

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")


SERVERS_FILE = "data/servers.json"
PREV_CHECKS = "data/PrevChecks.json"


def run_checks():
    print("server will be checked...")
    servers = load_servers(SERVERS_FILE)
    time = datetime.now()
    timeStr = f"{time.date()}  {time.strftime('%H:%M:%S')}"

    prev_checks = load_servers(PREV_CHECKS)
    for server in servers:
        addr = server["address"]
        status = ping_server(addr)
        server["status"] = status
        server["lastCheck"] = timeStr
        log.info(
            f"server: {addr} is pinged with status: {status}")
        prev_checks.append({
            "address": addr,
            "name": server["name"],
            "status": status,
            "lastCheck": timeStr
        })
    save_servers(servers, SERVERS_FILE)
    save_servers(prev_checks, PREV_CHECKS)


def ping_server(addr):
    print(f"{addr}: {ping(addr)}")
    response = ping(addr)
    if response != False and response != None:
        return "Online"
    else:
        return "Offline"


def generate_html_report():
    servers = load_servers(SERVERS_FILE)
    prev = load_servers(PREV_CHECKS)
    html_modification("reports/server_status_report.html", servers)
    html_modification("reports/server_prev_report.html", prev)


def html_modification(path, serverList):
    with open(path, "r") as html:
        template = html.read()

    div_start = template.find("<div>")
    div_end = template.find("</div>")
    div_data = template[div_start:div_end]

    updated_div = "<div><h2>Server name</h2><h2>Server Host</h2><h2>Server Status</h2><h2>last Check</h2>"
    for server in serverList:
        updated_div += f"<p>{server['name']}</p><p>{server['address']}</p><p>{server['status']}</p><p>{server['lastCheck']}</p>"

    report = template.replace(div_data, updated_div)

    with open(path, "w") as report_file:
        report_file.write(report)


def load_servers(loadFile):
    try:
        with open(loadFile, 'r') as file:
            servers = json.load(file)
    except (FileNotFoundError):
        log.exception("defined file is not found!")
        log.info(f"creating file {loadFile}")
        servers = []
    except (json.JSONDecodeError):
        log.exception(f"An error is found in {file.name}")
        sys.exit(1)
    return servers


def save_servers(servers, saveFile):
    with open(saveFile, 'w') as file:
        json.dump(servers, file)
