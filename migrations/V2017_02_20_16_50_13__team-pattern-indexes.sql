-- -*- sql-dialect: postgres; -*-
create index idx_team_patterns_for_team
on clippingsbot.team_patterns (team_id);

create index idx_team_patterns_for_channel
on clippingsbot.team_patterns (team_id, channel_id, created desc);
