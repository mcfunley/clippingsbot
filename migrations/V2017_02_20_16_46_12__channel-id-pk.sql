-- -*- sql-dialect: postgres; -*-
alter table clippingsbot.team_patterns drop constraint team_patterns_pkey;

alter table clippingsbot.team_patterns add primary key (team_id, pattern_id, channel_id);
