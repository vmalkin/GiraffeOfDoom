from instruments import MagnetometerLocalCSV, MagnetometerURL

rapid_run = MagnetometerLocalCSV("Ruru Rapidrun", "Vaughn", "Dunedin", "NULL", "C://test.csv")
goes = MagnetometerURL("GOES", "Vaughn", "Dunedin", "NULL", "http://www.test.com")

print(rapid_run.get_data())
print(goes.get_data())
