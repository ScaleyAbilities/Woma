import sys

fp = open(sys.argv[1], 'r')
# for each command line in the workload file, create JSON object and execute GET/POST to API
line = fp.readline()
output = set()
hash_bucket = {}
while line:
    uname = line.strip().split(' ')[1].split(',')[1]
    if uname[0] != '.':
        output.add(uname)
    line = fp.readline()

for name in output:
    letter = name[0]
    if letter in hash_bucket: 
        hash_bucket[letter] = hash_bucket[letter] + 1
    else:
        hash_bucket[letter] = 1

max = 0
min = 100000000

modulo = 5

for name in hash_bucket:
    if max < hash_bucket[name]:
        max = hash_bucket[name]

    if min > hash_bucket[name]:
        min = hash_bucket[name]

    print(name + " (" + str(ord(name) % modulo) + ") freq: " + str(hash_bucket[name]))

print("min freq: " + str(min) + "\nmax freq: " + str(max))
print("TOTAL NAMES: " + str(len(output)))