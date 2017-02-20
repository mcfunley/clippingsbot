-- -*- sql-dialect: postgres; -*-
alter table clippingsbot.team_patterns add column channel_id text not null;
