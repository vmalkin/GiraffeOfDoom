from time import time
a = ['GPGSV', '4', '3', '15', '08', '13', '268', '16', '01', '12', '218', '13', '27', '07', '303', '', '1$PMTK001', '220', '2']

b = ['GPGSV', '4', '1', '15', '32', '75', '278', '28', '10', '67', '089', '35', '193', '46', '279', '29', '23', '36', '074', '29']
c = ['GPGSV', '4', '2', '15', '20', '34', '065', '26', '21', '30', '231', '18', '24', '24', '132', '27', '31', '15', '353', '16']
d = ['GPGSV', '4', '3', '15', '08', '13', '268', '16', '01', '12', '218', '15', '27', '07', '303', '', '12', '05', '096', '15']
e = ['GPGSV', '4', '4', '15', '18', '02', '022', '', '25', '01', '060', '', '41', '', '', '']

class Satellite:
    def __init__(self, id):
        self.id = id
        self.alt = []
        self.az = []
        self.snr = []

    def create_s4(self):
        pass


gpgsv = []
for i in range(0, 500):
   gpgsv.append(Satellite(i))

glgsv = []
for i in range(0, 500):
    glgsv.append(Satellite(i))

def satlist_input(gsv_sentence):
    constellation = gsv_sentence[0]
    increment = 4
    for i in range(4, len(gsv_sentence) - 3, increment):
        satID = constellation + "_" + gsv_sentence[i]
        alt = gsv_sentence[i + 1]
        az = gsv_sentence[i + 2]
        snr = gsv_sentence[i + 3]
        gpgsv[satID].alt.append(alt)
        gpgsv[satID].az.append(az)
        gpgsv[satID].snr.append(snr)


if __name__ == "__main__":
    database_input(c)
