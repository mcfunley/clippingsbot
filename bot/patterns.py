from bot import db

def save(pattern):
    sql = """
    insert into clippingsbot.patterns (pattern)
    values (lower(:pattern))
    on conflict(lower(pattern)) do update
    set pattern = lower(:pattern)
    returning pattern_id
    """
    return db.scalar(sql, pattern=pattern)
