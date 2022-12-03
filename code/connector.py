import mysql.connector

from dbconfig import *


def set_up_db():
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
    )
    cursor = db.cursor()
    cursor.execute("create database IF NOT EXISTS mario")
    db.close()
    db = get_db()
    cursor = db.cursor()
    create_account_sql = 'create table if not exists Account(username varchar(24) primary key,password varchar(128) ' \
                         'not null, create_date timestamp DEFAULT CURRENT_TIMESTAMP , update_date timestamp DEFAULT ' \
                         'CURRENT_TIMESTAMP ); '
    cursor.execute(create_account_sql)
    create_game_data_sql = "create table if not exists gamedata(username varchar(24),coin int default 20,level int " \
                           "default 0,lock_time timestamp DEFAULT CURRENT_TIMESTAMP , create_date timestamp DEFAULT " \
                           "CURRENT_TIMESTAMP ,  update_date timestamp DEFAULT CURRENT_TIMESTAMP , constraint " \
                           "fk_account_gamedate foreign key(username) references account(username)) "
    cursor.execute(create_game_data_sql)
    db.close()


def get_db():
    return mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        db=db_name
    )
