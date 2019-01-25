import requests
import sys

# api endoing
API_ENDPOINT = '<url>'

fp = open('workload files' + str(sys.argv[1]), 'r')
# for each command line in the workload file, create JSON object and execute GET/POST to API
line = fp.readline()
while line:
    command = line[1].split(',')
    if command[0] == 'COMMIT_BUY' or 'CANCEL_BUY' or 'DISPLAY_SUMMARY':
        data = {
            'userid':command[1]
        }

    elif command[0] == 'ADD' or 'COMMIT_SELL' or 'CANCEL_SELL':
        data = {
            'userid':command[1],
            'amount':command[2]
        }

    elif command[0] == 'QUOTE' or 'CANCEL_SET_BUY' or 'CANCEL_SET_SELL':
        data = {
            'userid':command[1],
            'StockSymbol':command[2]
        }

    elif command[0] == 'BUY' or 'SELL' or 'SET_BUY_AMOUNT' or 'SET_BUY_TRIGGER' or 'SET_SELL_AMOUNT' or 'SET_SELL_TRIGGER':
        data = {
            'userid':command[1],
            'StockSymbol':command[2],
            'amount':command[3]
        }

    elif command[0] == 'DUMPLOG':
        if len(command) == 2:
            data = {
                'filename':command[1]
            }
        elif len(command) == 3:
            data = {
                'userid':command[1],
                'filename':command[2]
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
        requests.post(API_ENDPOINT, data)
    elif command[0] == 'QUOTE' or 'DUMPLOG' or 'DISPLAY_SUMMARY':
        requests.get(API_ENDPOINT, data)
    else:
        print('An error occured... BITTHHCCCHCH >:(')
