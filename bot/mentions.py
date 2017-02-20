from bot import db


def save(pattern, mention):
    sql = """
    insert into clippingsbot.mentions (
      pattern_id, feed, title, comments_url, link_url
    ) values (
      :pattern_id, :feed, :title, :comments_url, :link_url
    )
    on conflict (pattern_id, feed, link_url) do nothing
    """
    db.execute(
        sql, pattern_id=pattern['pattern_id'], feed=mention['feed'],
        title=mention['title'], comments_url=mention['comments_url'],
        link_url=mention['link_url']
    )
