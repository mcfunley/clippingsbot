-- -*- sql-dialect: postgres; -*-
alter table clippingsbot.notifications
  add column channel_id text not null,
  drop constraint notifications_pkey;

alter table clippingsbot.notifications
  add primary key (team_id, pattern_id, channel_id, feed, link_url);
