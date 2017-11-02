# -*- coding: utf-8 -*-
#from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import time, os, hashlib
import sqlite3

PENALTY = 20
Teams = {}
Chals = {}


def init():
    conn = sqlite3.connect('data.sqlite' ,check_same_thread = False)
    cursor = conn.cursor()

    cursor.execute( " SELECT name, id " + # id ==> ip
                    " FROM teams ")
    teams = cursor.fetchall()
    for team in teams:
        Teams[team[0]] = team[1]

    cursor.execute( " SELECT name, port FROM chals ")
    chals = cursor.fetchall()
    for chal in chals:
        Chals[chal[0]] = chal[1]

    cursor.close()
    conn.close()


def getFlag(ip, chal):
    stime = int(time.time()) // 10
    data = str(stime) + str(ip) + str(chal)
    md5 = hashlib.md5(data.encode('utf-8')).hexdigest()
    flag = "flag{" + md5[15:25] + "}"
    return flag


def updateFlag():
    conn = sqlite3.connect('data.sqlite', check_same_thread = False)
    cursor = conn.cursor()

    for team, ip in Teams.items():
        for chal in Chals.keys():
            flag_next = getFlag(ip, chal)
            cursor.execute( " UPDATE flags " +
                            " SET flag_now = '" + flag_next + "' " +
                            " WHERE team_name = '" + team + "' " +
                            " AND chal_name = '" + chal + "' "
                            )

    cursor.close()
    conn.commit()
    conn.close()


def pwnCheck(ip, port):
    return 0


def checkService():
    conn = sqlite3.connect('data.sqlite', check_same_thread = False)
    cursor = conn.cursor()

    for team, ip in Teams.items():

        count = pwnCheck(ip, int(Chals['pwn']))

        if count:
            cursor.execute( " SELECT score FROM teams " +
                            " WHERE team_name = '" + team + "' "
                            )
            score = int(cursor.fetchone()[0])
            score -= count * PENALTY
            cursor.execute( " UPDATE teams " +
                            " SET score = " + str(score) + " " +
                            " WHERE team_name = '" + team + "' "
                            )

    cursor.close()
    conn.commit()
    conn.close()


init()
#sched = BackgroundScheduler()
sched = BlockingScheduler()
sched.add_job(updateFlag, 'interval', seconds=5*60)
sched.start()
