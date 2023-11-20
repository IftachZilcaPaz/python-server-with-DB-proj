import socket
import random
import sqlite3
import datetime
import json

SERVER_ADDRESS = '127.0.0.1', 54322
DB_PATH = "station_status.sqlite3"


def date():
    last_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return last_date


def get_values_to_sql(req: bytes) -> bytes:
    try:
        dat = date()
        dat1 = dat
        req = req.decode()
        req = json.loads(req)
        st = int(req['station_id'])
        a1 = str(req['alr1'])
        a2 = str(req['alr2'])
        #resp_str = (st, a1, a2)
        resp_str = f"{st}, {a1}, {a2}, {dat1}"
    except UnicodeDecodeError:
        resp_str = 'error: not utf-8 encoded'
    except json.JSONDecodeError:
        resp_str = 'error: not json'
    except ValueError:
        resp_str = 'error: invalid response'
    except KeyboardInterrupt:
        pass

    return resp_str.encode('utf-8')


def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.bind(SERVER_ADDRESS)
            while True:
                print('Waiting for connection...')
                req, addr = s.recvfrom(1024)
                resp = get_values_to_sql(req)

                resp_new = resp.decode('utf-8')

                values = resp_new.split(", ")
                st = int(values[0])
                a1 = values[1]
                a2 = values[2]
                dat = values[3]
                print(st, a1, a2, dat)
                print()

                s.sendto(resp, addr)

                print('Checking if table are exists...')
                with sqlite3.connect(DB_PATH) as con:
                    curs = con.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='station_status'")
                result = curs.fetchone()
                if result is not None:
                    print("---Table are exists---")
                else:
                    print("---Table does not exist---")
                    print("Creating new table....")
                    con.execute("""CREATE TABLE IF NOT EXISTS station_status (
                                                        station_id INTEGER PRIMARY KEY,
                                                        last_date TEXT,
                                                        alarm1 INT,
                                                        alarm2 INT
                                                         );""")
                with sqlite3.connect(DB_PATH) as con:
                    curs = con.execute("""
                    INSERT
                    OR
                    REPLACE
                    INTO
                    station_status
                    VALUES(?, ?, ?, ?);
                    """, (st, dat, a1, a2))
    except KeyboardInterrupt:
        s.close()


if __name__ == "__main__":
    main()
