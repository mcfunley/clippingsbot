from bot import db, team, monitor
import requests
from slackclient import SlackClient


pending_sql = """
select m.pattern_id, m.feed, m.title, m.comments_url, m.link_url,
  tp.team_id, tp.channel_id, tp.display_pattern
from clippingsbot.mentions m
left join clippingsbot.team_patterns tp on m.pattern_id = tp.pattern_id
where team_id is not null and not exists (
  select 1
  from clippingsbot.notifications n
  where n.team_id = tp.team_id
    and n.pattern_id = tp.pattern_id
    and n.feed = m.feed
    and n.comments_url = m.comments_url
    and n.channel_id = tp.channel_id
)
order by m.created asc limit 50;
"""


def message(pending_notification):
    if pending_notification['feed'] == 'homepage':
        fmt = ('A mention of `%s` made the Hacker News homepage: \n'
               '<%s|%s> [<%s|comments>]')
    elif pending_notification['feed'] == 'newest':
        fmt = ('New submission mentioning `%s` on Hacker News: \n'
               '<%s|%s> [<%s|comments>]')

    return fmt % (
        pending_notification['display_pattern'],
        pending_notification['link_url'],
        pending_notification['title'],
        pending_notification['comments_url'],
    )


def post(pending_notification):
    t = team.find(pending_notification['team_id'])
    c = SlackClient(t['access_token'])
    c.api_call(
        'chat.postMessage',
        channel=pending_notification['channel_id'],
        text=message(pending_notification),
        unfurl_links=False
    )


def record(pending_notification):
    sql = """
    insert into clippingsbot.notifications (
      team_id, pattern_id, channel_id, feed, comments_url, link_url
    ) values (
      :team_id, :pattern_id, :channel_id, :feed, :comments_url, :link_url
    )
    on conflict (team_id, pattern_id, channel_id, feed, comments_url)
    do update set created = current_timestamp
    """
    db.execute(
        sql,
        team_id=pending_notification['team_id'],
        pattern_id=pending_notification['pattern_id'],
        channel_id=pending_notification['channel_id'],
        feed=pending_notification['feed'],
        link_url=pending_notification['link_url'],
        comments_url=pending_notification['comments_url'],
    )

def run():
    sent = 0
    for pending_notification in db.find(pending_sql):
        sent += 1
        post(pending_notification)
        record(pending_notification)

    if sent > 0:
        monitor.notify('notifier sent %s notifications' % sent)
