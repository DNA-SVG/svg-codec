import os
svg_dir = './test_result/'
dirs = [f for f in os.listdir(svg_dir) if not f.startswith('.')]
total_stat = {}
for dir in dirs:
    result = {}
    for filename in os.listdir(os.path.join(svg_dir, dir)):
        if filename.endswith('.csv'):
            result[filename[:-4]] = {}
            with open(os.path.join(svg_dir, dir, filename), 'r') as file:
                for line in file:
                    content = line.strip().split(',')
                    result[filename[:-4]][content[0]] = content[1]
    result_new = {}
    for a, b_dict in result.items():
        for b, c in b_dict.items():
            if b not in result_new:
                result_new[b] = []
            result_new[b].append(int(c))
    tmp = []
    for a, b in result_new.items():
        tmp.append(1 - b[1] * 1.5 / b[0] / 8)
    total_stat[dir] = []
    total_stat[dir].append(sum(tmp) / len(tmp))

total_stat = dict(sorted(total_stat.items(), key=lambda item: item[0]))

with open('stat.csv', 'w') as file:
    file.write(
        'name,default vs gzip\n'
    )
    for key in total_stat:
        file.write(key + ',' + ','.join([str(x) for x in total_stat[key]]) + '\n')