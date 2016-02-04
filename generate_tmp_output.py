from os import listdir
from os.path import isfile, join

filenames = [f for f in listdir('output') if isfile(join('output', f))]
for filename in filenames:
    lines = []
    count = 0
    f = open('output/' + filename, 'r')
    for line in f:
        lines.append(line)
        count = count + 1
        if (count == 100):
            break
    f.close()

    f = open('tmp_output/' + filename, 'w')
    for line in lines:
        f.write(line)
    f.close()
