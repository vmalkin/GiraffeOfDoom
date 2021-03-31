-- SQLite
create table testalerts(
datetime integer,
station text,
message text
);


insert into testalerts (datetime, station, message) values (1000, "st1", "st 1normal 1000");
insert into testalerts (datetime, station, message) values (1001, "st1", "st1 disturbed 1001");
insert into testalerts (datetime, station, message) values (1001, "st2", "st2 normal 1001");
insert into testalerts (datetime, station, message) values (1003, "st3", "st3 normal 1003");
insert into testalerts (datetime, station, message) values (1004, "st1", "st1 disturbed 1004");
insert into testalerts (datetime, station, message) values (1004, "st2", "st2 normal 1004");
insert into testalerts (datetime, station, message) values (1005, "st1", "st1 alert 1005");
insert into testalerts (datetime, station, message) values (1006, "st3", "st3 normal 1006");

select * from testalerts;
select max(datetime), station, message from testalerts where datetime > 1002 group by station ;