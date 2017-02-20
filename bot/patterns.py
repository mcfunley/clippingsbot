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

def find_all():
    return db.find("""
        select *
        from clippingsbot.patterns p
        where exists (
          select 1 from clippingsbot.team_patterns tp
          where tp.pattern_id = p.pattern_id
        )""")
