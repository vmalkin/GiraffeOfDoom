from enum import Enum


class State(Enum):
    SETUP = 0
    GET_DATA = 1
    VERIFY_DATA = 2
    ADD_DATA = 3
    ERROR = 4


current_state = State.SETUP
current_message = None

if __name__ == "__main__":
    # Set up non-blocking timing.
    while True:

# check_create_udp_socket()
# check_create_folders()
# check_create_db()
# get_data()
# verify_data()
# add_data()



