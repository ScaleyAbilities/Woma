import requests
import sys
import time

API_ENDPOINT = 'http://127.0.0.1:80/api/command'

num = 1

program_time = time.perf_counter()
requests_time = 0

# Use a session so that we keep the connection alive
s = requests.Session()

fp = open(sys.argv[1], 'r')
# for each command line in the workload file, create JSON object and execute GET/POST to API
line = fp.readline()
while line:
    command = line.strip().split(' ')[1].split(',')
    # print(command)
    if command[0] == 'COMMIT_BUY' or command[0] == 'CANCEL_BUY' or command[0] == 'COMMIT_SELL' or command[0] == 'CANCEL_SELL' or command[0] == 'DISPLAY_SUMMARY':
        data = {
            'cmd': command[0],
            'usr': command[1]
        }

    elif command[0] == 'ADD':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'amount': command[2]
            }
        }


    elif command[0] == 'QUOTE' or command[0] == 'CANCEL_SET_BUY' or command[0] == 'CANCEL_SET_SELL':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'stock': command[2]
            }
        }

    elif command[0] == 'BUY' or command[0] == 'SELL' or command[0] == 'SET_BUY_AMOUNT' or command[0] == 'SET_SELL_AMOUNT':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'stock': command[2],
                'amount': command[3]
            }
        }

    elif command[0] == 'SET_BUY_TRIGGER' or command[0] == 'SET_SELL_TRIGGER':
        data = {
            'cmd': command[0],
            'usr': command[1],
            'params': {
                'stock': command[2],
                'price': command[3]
            }
        }

    elif command[0] == 'DUMPLOG':
        if len(command) == 2:
            data = {
                'cmd': command[0],
                'usr': None,
                'params': {
                    'filename': command[1]
                }
            }
        elif len(command) == 3:
            data = {
                'cmd': command[0],
                'usr': command[1],
                'params': {
                    'filename': command[2]
                }
            }
        else:
            print('DUMPLOG parameters unexpected, input: ' + command)

    else:
        print('Command not recognized: ' + command[0])

    request_timer = time.perf_counter()
    s.post(API_ENDPOINT, headers={'Content-Type': 'application/json'}, data=None, json=data)
    requests_time += time.perf_counter() - request_timer

    sys.stdout.write('Sent Request %d\r' % num)
    num += 1

    line = fp.readline()

fp.close()

print('Total program time:     %.5f sec' % (time.perf_counter() - program_time))
print('Time spent on requests: %.5f sec' % requests_time)
