import os
import json

from ping3 import ping
from datetime import datetime

SERVERS_FILE = "data/servers.json"
PREV_CHECKS = "data/PrevChecks.json"


def run_checks():
    print("server will be checked...")
    servers = load_servers()
    time = datetime.now()
    timeStr = f"{time.date()}  {time.strftime('%H:%M:%S')}"

    for server in servers:
        addr = server["address"]
        status = ping_server(addr)
        server["status"] = status
        server["lastCheck"] = timeStr
    save_servers(servers)


def ping_server(addr):
    print(f"{addr}: {ping(addr)}")
    response = ping(addr)
    if response != False:
        return "Online"
    else:
        return "Offline"


def generate_html_report():
    servers = load_servers()

    with open("reports/server_status_report.html", "r") as html:
        template = html.read()

    div_start = template.find("<div>")
    div_end = template.find("</div>")
    div_data = template[div_start:div_end]

    updated_div = "<div><h2>Server name</h2><h2>Server Host</h2><h2>Server Status</h2><h2>last Check</h2>"
    for server in servers:
        updated_div += f"<p>{server['name']}</p><p>{server['address']}</p><p>{server['status']}</p><p>{server['lastCheck']}</p>"

    report = template.replace(div_data, updated_div)

    with open("reports/server_status_report.html", "w") as report_file:
        report_file.write(report)


def load_servers():
    try:
        with open(SERVERS_FILE, 'r') as file:
            servers = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        servers = []
    return servers


def save_servers(servers):
    with open(SERVERS_FILE, 'w') as file:
        json.dump(servers, file)
