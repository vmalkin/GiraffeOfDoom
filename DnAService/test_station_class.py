import unittest
import Station

# ##################################
# Unit test File for Station Class
# ##################################
station_details = ("Ruru Observatory Rapid-run magnetometer", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30)
test_station = Station.Station(station_details)

class pickletest(unittest.TestCase):
    def test_pickleload(self):
        test_array = test_station.loadpickle()
        self.assertTrue(len(test_array) > 0)

    def test_get_data_from_source(self):
        test_array = test_station.get_data()
        self.assertTrue(len(test_array) > 0)

    def test_utc2unix_conversion(self):
        input_array = ["2017-10-05 02:06:08.1,10", "2017-10-05 02:06:08.1,20"]
        answer_array = ["1507122368.0,10","1507122368.0,20"]
        test_answer = test_station.utc2unix(input_array)
        self.assertCountEqual(test_answer, answer_array)

    def test_create_dadt(self):
        pass

if __name__ =="__main__":
    unittest.main()
