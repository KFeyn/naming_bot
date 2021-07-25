drop table if exists names.default_names;
create  table names.default_names ("id" bytea, "fio" character varying, "rating" float, "games" integer);
create unique index UI_default_names_id on names.default_names ("id");

insert into names.default_names values (md5('Бобби Котик')::bytea, 'Бобби Котик', 0, 0),
(md5('Владимир Противень')::bytea, 'Валерий Писиксен', 0, 0);

drop table if exists names.users;
create table names.users ("telegram_id" integer, "fio" character varying);
create unique index UI_names_telegram_id on names.users ("telegram_id");

drop table if exists names.pairs;
create table names.pairs as
select
	 md5(dn1.fio || '-' || dn2.fio)::bytea "pair"
	 ,dn1.fio || '-' || dn2.fio "fio_pair"
	 ,ARRAY[]::integer[] "users"
from
	names.default_names dn1
join
	names.default_names dn2
		on dn1.id > dn2.id;

	
	