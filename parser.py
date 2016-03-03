import sqlite3 as lite
import os
from bs4 import BeautifulSoup
import requests


def save_to_database():

    con = lite.connect('/home/ec2-user/git/first_robotics/db.sqlite3')

    # <h1 itemprop="summary">San Diego Regional 2016</h1>
    # [<h1 itemprop="summary">Greater Toronto Central Regional 2016</h1>]
    # line[0].get_text()

    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS teams_by_event(
            id INTEGER PRIMARY KEY, team_number INT,
                event_name TEXT, shorthand TEXT);
    """)
    cur.close()
    base_url = "http://www.thebluealliance.com/event/"
    for folder_name in os.listdir("."):
        if os.path.isdir(folder_name) and folder_name.startswith("2"):
            url = base_url + folder_name
            print folder_name, url
            for subdir, dirs, files in os.walk(folder_name):
                for file in files:
                    with open(subdir + "/" + file, "r") as f:
                        data = f.read()
                    line = data.strip().split(",")
                    for entry in line:
                        resp = requests.get(url=url)
                        data = resp.content
                        soup = BeautifulSoup(data, "html.parser")
                        texts = soup.findAll('h1')
                        if len(texts) > 0:
                            event_name = texts[0].get_text()
                        else:
                            event_name = "NOT FOUND"
                        team_number = int(entry.lstrip("frc"))
                        cur = con.cursor()
                        cur.execute("""
                            INSERT INTO teams_by_event(
                                id, team_number, event_name, shorthand)
                                    VALUES(NULL, ?, ?, ?);
                        """, [team_number, event_name, folder_name])
                        cur.close()
                        con.commit()
    return

if __name__ == "__main__":
    save_to_database()
