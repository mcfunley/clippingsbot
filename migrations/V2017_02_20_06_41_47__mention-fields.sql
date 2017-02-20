-- -*- sql-dialect: postgres; -*-
drop table clippingsbot.mentions;

create table clippingsbot.mentions (
  pattern_id bigint not null references clippingsbot.patterns (pattern_id),
  feed text not null,
  title text not null,
  comments_url text not null,
  link_url text not null,
  created timestamp with time zone not null default current_timestamp,
  primary key (pattern_id, feed, link_url)
);


drop table clippingsbot.notifications;

create table clippingsbot.notifications (
  team_id text not null references clippingsbot.teams (team_id),
  pattern_id bigint not null references clippingsbot.patterns (pattern_id),
  feed text not null,
  link_url text not null,

  created timestamp with time zone not null default current_timestamp,

  primary key (team_id, pattern_id, feed, link_url)
);
