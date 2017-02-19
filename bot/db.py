import os
from sqlalchemy import create_engine
from sqlalchemy.sql import text

dburl = '%s?user=%s&password=%s' % (
    os.getenv('DATABASE_URL'),
    os.getenv('DATABASE_USER'),
    os.getenv('DATABASE_PASSWORD'))

engine = create_engine(dburl)


def connect():
    return engine.connect()


def execute(sql, **args):
    return engine.execute(text(sql), **args)


def find_one(sql, **args):
    r = execute(sql, **args)
    return { k: v for k, v in zip(r.keys(), r.first()) }


def find(sql, **args):
    r = execute(sql, **args)
    ks = r.keys()
    return ({ k: v for k, v in zip(ks, row)} for row in r.fetchall())


def scalar(sql, **args):
    r = execute(sql, **args).first()
    if r:
        return r[0]
    return None
