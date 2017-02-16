-- -*- sql-dialect: postgres; -*-

-- teams get created when the button is clicked.
-- they add patterns with a /command
-- we periodically crawl, and find mentions of patterns.
-- each team subscribed to a pattern gets a notification when it's mentioned

create table clippingsbot.teams (
  team_id text primary key,
  access_token text not null,
  user_id text not null,
  team_name text not null,
  scope text not null
);

create table clippingsbot.patterns (
  pattern_id bigserial not null primary key,
  pattern text not null,
  created timestamp with time zone not null default current_timestamp
);

create unique index idx_pattern_lower_unique on clippingsbot.patterns (lower(pattern));

create table clippingsbot.team_patterns (
  team_id text not null references clippingsbot.teams (team_id),
  pattern_id bigint not null references clippingsbot.patterns (pattern_id),
  display_pattern text not null,

  created timestamp with time zone not null default current_timestamp,
  primary key (team_id, pattern_id)
);

create index idx_team_patterns_sorted
on clippingsbot.team_patterns (team_id, created desc);

create table clippingsbot.mentions (
  pattern_id bigint not null references clippingsbot.patterns (pattern_id),
  discussion_url text not null,
  reference_url text,
  created timestamp with time zone not null default current_timestamp,
  primary key (pattern_id, discussion_url)
);

create table clippingsbot.notifications (
  team_id text not null references clippingsbot.teams (team_id),
  pattern_id bigint not null references clippingsbot.patterns (pattern_id),
  discussion_url text not null,

  created timestamp with time zone not null default current_timestamp,

  primary key (team_id, pattern_id, discussion_url)
);
