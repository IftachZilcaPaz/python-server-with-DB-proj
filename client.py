import socket
import os
import json
import random
from os.path import exists
from time import sleep

SERVER_ADDRESS = '127.0.0.1', 54322
FILENAME = "status.txt"


def get_random():
    status_tup = {
        'station_id': int(random.randint(100, 999)),
        'alr1': str(random.randint(0, 1)),
        'alr2': str(random.randint(0, 1))
    }
    return status_tup


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            while True:
                try:
                    with open(FILENAME, 'w') as status:
                        status_tup = {
                            'station_id': int(random.randint(100, 999)),
                            'alr1': str(random.randint(0, 1)),
                            'alr2': str(random.randint(0, 1))
                        }
                        status.write(str(status_tup['station_id']) + ' ')
                        status.write((status_tup['alr1']) + ' ')
                        status.write((status_tup['alr2']) + ' ')
                    with open(FILENAME, 'r') as status:
                        content = status.readline()
                        station_id, alr1, alr2 = content.split()
                        if alr1 == alr2:
                            continue
                    equation = {
                        'station_id': station_id,
                        'alr1': alr1,
                        'alr2': alr2
                    }

                    req = json.dumps(equation).encode()
                    s.sendto(req, SERVER_ADDRESS)
                    print('Message sent to server')
                    response = s.recv(1024)
                    print('Message received')

                    print(response.decode())
                    sleep(10)
                except ValueError:
                    print("error, value/s not valid")
        except KeyboardInterrupt:
            pass



if __name__ == '__main__':
    main()
