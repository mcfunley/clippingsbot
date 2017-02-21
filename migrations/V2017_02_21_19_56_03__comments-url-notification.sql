-- -*- sql-dialect: postgres; -*-
alter table clippingsbot.mentions
  drop constraint mentions_pkey;

alter table clippingsbot.mentions
  add primary key (pattern_id, feed, comments_url);

alter table clippingsbot.notifications
  add column comments_url text not null,
  drop constraint notifications_pkey;

alter table clippingsbot.notifications
  add primary key (team_id, pattern_id, channel_id, feed, comments_url);
