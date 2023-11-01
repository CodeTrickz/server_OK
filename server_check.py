import os
import json

from ping3 import ping
from datetime import datetime

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
    if response != False:
        return "Online"
    else:
        return "Offline"


def generate_html_report():
    servers = load_servers(SERVERS_FILE)
    prev = load_servers(PREV_CHECKS)

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

    with open("reports/server_prev_report.html", "r") as html2:
        template2 = html2.read()

    div_start2 = template2.find("<div>")
    div_end2 = template2.find("</div>")
    div_data2 = template2[div_start2:div_end2]

    updated_div2 = "<div><h2>Server name</h2><h2>Server Host</h2><h2>Server Status</h2><h2>last Check</h2>"
    for previous in prev:
        updated_div2 += f"<p>{previous['name']}</p><p>{previous['address']}</p><p>{previous['status']}</p><p>{previous['lastCheck']}</p>"

    report2 = template2.replace(div_data2, updated_div2)

    with open("reports/server_prev_report.html", "w") as report_file2:
        report_file2.write(report2)


def load_servers(loadFile):
    try:
        with open(loadFile, 'r') as file:
            servers = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        servers = []
    return servers


def save_servers(servers, saveFile):
    with open(saveFile, 'w') as file:
        json.dump(servers, file)
