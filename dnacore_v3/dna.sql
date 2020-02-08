
drop table if exists station;
drop table if exists station_data;
PRAGMA foreign_keys = ON;

create table station (
station_id text not null primary key
);

create table station_data(
station_id text,
data_value text,
foreign key (station_id) references station(station_id)
);

insert into station(station_id) values ("Ruru_Obs");
insert into station(station_id) values ("Dn_Aurora");
insert into station(station_id) values ("GOES_16");
insert into station(station_id) values ("Geomag_Bz");
insert into station(station_id) values ("SW_speed");
insert into station(station_id) values ("SW_Density");