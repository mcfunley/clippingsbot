select m.pattern_id, m.feed, m.title, m.comments_url, m.link_url,
  tp.team_id, tp.channel_id
from clippingsbot.mentions m
left join clippingsbot.team_patterns tp on m.pattern_id = tp.pattern_id
where not exists (
  select 1
  from clippingsbot.notifications n
  where n.team_id = tp.team_id
    and n.pattern_id = tp.pattern_id
    and n.feed = m.feed
    and n.link_url = m.link_url
    and n.channel_id = tp.channel_id
)
order by m.created asc;
