#!"/home/kip/Dropbox/Programming/Python/TimGamingAlert Repo/TimGamingAlert/venv/bin/python"

import os
from pathlib import Path
from mcstatus import JavaServer
import json
from dasbus.connection import SessionMessageBus


def main():
    save_dir = os.environ.get("HOME") + "/.server_admin"
    save_file = "current_players.txt"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)


    old_set = set()
    if os.path.exists(save_dir+'/'+save_file):
        with open(save_dir+'/'+save_file) as f:
            t = json.loads(f.read())
            old_set = set(t)

    server = JavaServer.lookup("timgaming.com")
    query = server.query()
    current_set = set(query.players.names)
    #print("The server has the following players online: {0}".format(", ".join(current_set)))

    message = ""
    new_player_set = current_set.difference(old_set)
    if len(new_player_set):
        new_player_string = ", ".join(new_player_set)
        message = message + new_player_string + " logged on"
        print(f"Online players: {new_player_string}")

    left_player_set = old_set.difference(current_set)
    if len(left_player_set):
        left_player_string = ", ".join(left_player_set)
        message = message + left_player_string + " logged out"
        print(f"Offline players: {left_player_string}")

    if len(message):
        os.environ['DBUS_SESSION_BUS_ADDRESS'] = 'unix:path=/run/user/1000/bus'
        os.environ['DISPLAY'] = ':0'
        
        bus = SessionMessageBus()
        proxy = bus.get_proxy(
            "org.freedesktop.Notifications",
            "/org/freedesktop/Notifications"
        )

        id = proxy.Notify(
            "", 0, "applications-games", "Tim Gaming Notification",
            message,
            [], {}, 0
        )

    #Save current list for next time
    with open(save_dir+"/"+save_file,'w') as f:
        f.write(json.dumps(list(current_set)))
    f.close()

if __name__ == '__main__':
    main()