import kindexer

posixarray = []
with open("arraysave.csv") as e:
    for line in e:
        line = line.strip()  # remove any trailing whitespace chars like CR and NL
        posixarray.append(line)

station1 = kindexer.Station("RuruRapid", posixarray, "\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d.\d\d", "%Y-%m-%d %H:%M:%S.%f")
station1.process_data()

