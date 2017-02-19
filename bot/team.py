from bot import db

def save(data):
    sql = """
    insert into clippingsbot.teams (
      team_id, access_token, user_id, team_name, scope
    ) values (
      :team_id, :access_token, :user_id, :team_name, :scope
    ) on conflict (team_id) do update
      set scope = excluded.scope,
          access_token = excluded.access_token,
          user_id = excluded.user_id,
          team_name = excluded.team_name

    returning team_id
    """
    return db.scalar(sql, **data)


def find(team_id):
    return db.find_one(
        'select * from clippingsbot.teams where team_id = :team_id',
        team_id = team_id)


def watch(team, pattern, pattern_id):
    sql = """
    insert into clippingsbot.team_patterns (team_id, pattern_id, display_pattern)
    values (:team_id, :pattern_id, :pattern)
    on conflict (team_id, pattern_id) do nothing
    """
    db.execute(
        sql, team_id=team['team_id'], pattern_id=pattern_id, pattern=pattern
    )


def find_patterns(team):
    sql = """
    select * from clippingsbot.team_patterns where team_id = :team_id
    """
    return db.find(sql, team_id=team['team_id'])


def count_patterns(team):
    sql = """
    select count(*) from clippingsbot.team_patterns where team_id = :team_id
    """
    return db.scalar(sql, team_id=team['team_id'])


def stop(team, pattern):
    sql = """
    delete from clippingsbot.team_patterns
    where team_id = :team_id and lower(display_pattern) = lower(:pattern)
    """
    db.execute(sql, team_id=team['team_id'], pattern=pattern)
