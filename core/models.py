import sqlite3 as sql
import datetime


def insertUser(name, surname, username, password):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (Name, Surname, Username, Password, RegisterDate LastLoginDate) VALUES (?,?)",
                (name, surname, username, password, datetime.datetime.now(), datetime.datetime.now()))
    con.commit()
    con.close()


def retrieveUsers():
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT username, password FROM users")
    users = cur.fetchall()
    con.close()
    return users
