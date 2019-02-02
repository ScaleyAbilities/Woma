import requests
import sys

API_ENDPOINT = 'http://127.0.0.1:80/api/command'

fp = open('workload files/' + str(sys.argv[1]), 'r')
# for each command line in the workload file, create JSON object and execute GET/POST to API
line = fp.readline()
while line:
    command = line.split(' ')[1].split(',')
    # print(command)
    if command[0] == 'COMMIT_BUY' or command[0] == 'CANCEL_BUY' or command[0] == 'COMMIT_SELL' or command[0] == 'CANCEL_SELL' or command[0] == 'DISPLAY_SUMMARY':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'userid': command[1]
            }
        }

    elif command[0] == 'ADD':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'userid': command[1],
                'amount': command[2]
            }
        }


    elif command[0] == 'QUOTE' or command[0] == 'CANCEL_SET_BUY' or command[0] == 'CANCEL_SET_SELL':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'userid': command[1],
                'stockSymbol': command[2]
            }
        }

    elif command[0] == 'BUY' or command[0] == 'SELL' or command[0] == 'SET_BUY_AMOUNT' or command[0] == 'SET_BUY_TRIGGER' or command[0] == 'SET_SELL_AMOUNT' or command[0] == 'SET_SELL_TRIGGER':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'userid': command[1],
                'stockSymbol': command[2],
                'amount': command[3]
            }
        }

    elif command[0] == 'DUMPLOG':
        if len(command) == 2:
            data = {
                'cmd': command[0],
                'usr': command[1],
                'params': {
                    'filename': command[1]
                }
            }
        elif len(command) == 3:
            data = {
                'cmd': command[0],
                'usr': command[1],
                'params': {
                    'userid': command[1],
                    'filename': command[2]
                }
            }
        else:
            print('DUMPLOG parameters unexpected, input: ' + command)

    else:
        print('Command not recognized: ' + command[0])

    # post requests
    if command[0] == 'ADD' or 'BUY' or 'COMMIT_BUY' or 'CANCEL_BUY'\
                        or 'SELL' or 'COMMIT_SELL' or 'CANCEL_SELL'\
                        or 'SET_BUY_AMOUNT' or 'CANCEL_SET_BUY' or 'SET_BUY_TRIGGER'\
                        or 'SET_SELL_AMOUNT' or 'CANCEL_SET_SELL' or 'SET_SELL_TRIGGER':
        # print(data)
        # print(requests.post(API_ENDPOINT, headers={'Content-Type': 'application/json'}, data=None, json=data))
        requests.post(API_ENDPOINT, headers={'Content-Type': 'application/json'}, data=None, json=data)
    elif command[0] == 'QUOTE' or 'DUMPLOG' or 'DISPLAY_SUMMARY':
        requests.get(API_ENDPOINT, data)
    else:
        print('unexpected request...')

    line = fp.readline()

fp.close()
