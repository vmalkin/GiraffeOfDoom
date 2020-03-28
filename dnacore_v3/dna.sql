
drop table if exists station;
drop table if exists station_data;
PRAGMA foreign_keys = ON;

create table station (
station_id text not null primary key
);

create table station_data(
station_id text,
posix_time text,
data_value text,
foreign key (station_id) references station(station_id)
);

insert into station(station_id) values ("Ruru_Obs");
insert into station(station_id) values ("Dn_Aurora");
insert into station(station_id) values ("GOES_16");
insert into station(station_id) values ("Geomag_Bz");
insert into station(station_id) values ("SW_speed");
insert into station(station_id) values ("SW_Density");

insert into station_data(station_id, posix_time, data_value) values ("Ruru_Obs", "1585307908", "-40.172");
insert into station_data(station_id, posix_time, data_value) values ("Ruru_Obs", "1585307910", "-40.176");
insert into station_data(station_id, posix_time, data_value) values ("Ruru_Obs", "1585307912", "-40.174");
insert into station_data(station_id, posix_time, data_value) values ("Ruru_Obs", "1585307915", "-40.168");

insert into station_data(station_id, posix_time, data_value) values ("GOES_16", "1585307909", "140.172");
insert into station_data(station_id, posix_time, data_value) values ("GOES_16", "1585307911", "140.176");
insert into station_data(station_id, posix_time, data_value) values ("GOES_16", "1585307914", "140.174");
insert into station_data(station_id, posix_time, data_value) values ("GOES_16", "1585307916", "140.168");