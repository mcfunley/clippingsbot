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
    return db.connect().query(sql, **data).next()[0]

def find(team_id):
    return db.connect().query("""
    select * from clippingsbot.teams where team_id = :team_id
    """, team_id = team_id).next()
