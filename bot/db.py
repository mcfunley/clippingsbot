import os
import records

dburl = '%s?user=%s&password=%s' % (
    os.getenv('DATABASE_URL'),
    os.getenv('DATABASE_USER'),
    os.getenv('DATABASE_PASSWORD'))

def connect():
    return records.Database(dburl)
