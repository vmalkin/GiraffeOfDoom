import unittest
import Station

# ##################################
# Unit test File for Station Class
# ##################################
test_station = Station.Station("Ruru Observatory", "http://www.ruruobservatory.org.nz/dr01_1hr.csv", "w3", "%Y-%m-%d %H:%M:%S.%f", 30,100)

class pickletest(unittest.TestCase):
    # def test_pickleload(self):
    #     test_array = test_station.loadpickle()
    #     self.assertTrue(len(test_array) > 0)

    # def test_get_data_from_source(self):
    #     test_array = test_station.get_data()
    #     self.assertTrue(len(test_array) > 0)

    def test_utc2unix_conversion(self):
        input_array = ["2017-10-05 02:06:08.1,10", "2017-10-05 02:06:08.1,20"]
        answer_array = ["1507122368.0,10","1507122368.0,20"]
        test_answer = test_station.utc2unix(input_array)
        self.assertCountEqual(test_answer, answer_array)

    def test_create_dadt(self):
        input_array = [
            "1507122368.0, 10",
            "1507122378.0, 11",
            "1507122388.0, 12",
            "1507122398.0, 11",
            "1507122408.0, 10"
        ]

        answer_array = [
            "1507122378.0,1.0",
            "1507122388.0,1.0",
            "1507122398.0,-1.0",
            "1507122408.0,-1.0"
        ]

        test_answer = test_station.create_dadt(input_array)
        self.assertCountEqual(answer_array, test_answer)

    def test_reconstruct_readings(self):
        input_array = [
            "1507122378.0,1",
            "1507122388.0,1",
            "1507122398.0,-1",
            "1507122408.0,-1"
        ]

        answer_array = [
            "1507122378.0,1.0",
            "1507122388.0,2.0",
            "1507122398.0,1.0",
            "1507122408.0,0.0"
        ]

        test_answer = test_station.rebuild_from_dadt(input_array)
        self.assertCountEqual(answer_array, test_answer)


    def test_aggregate_new_data(self):
        current_data = [
            "1507122378.0, 1",
            "1507122388.0, 1",
            "1507122398.0, -1",
            "1507122408.0, -1"]

        new_data = [
            "1507122398.0, -1",
            "1507122408.0, -1",
            "1507122418.0, -1",
            "1507122428.0, -1"]

        test_answer = [
            "1507122378.0, 1",
            "1507122388.0, 1",
            "1507122398.0, -1",
            "1507122408.0, -1",
            "1507122418.0, -1",
            "1507122428.0, -1"]

        answer_data = test_station.aggregate_new_data(current_data, new_data)
        self.assertCountEqual(test_answer, answer_data)

if __name__ =="__main__":
    unittest.main()
