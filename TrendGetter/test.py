import kindexer

station1 = kindexer.Station("aurora_activity", "files.txt", "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d", "%Y-%m-%d %H:%M:%S")

print("2018-05-02 00:00:54,1525219254.0460246")

print(station1.posix_to_utc(1525219254.0460246, "%Y-%m-%d"))

