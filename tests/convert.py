import os
import re
from copy import deepcopy
import dictdatabase as ddb

test = 1
for file in os.listdir():
    if file == 'convert.py': continue
    
    with open(file) as s:
        txt = iter(s.read().split('\n\n'))
        json = { }
        
        try:
            line = next(txt)
        except StopIteration:
            break
        
        for i in range(6):
            matched = re.match(r'([\w]+[_[\w]+]*): ([0-9]+) ', line)
            if matched:
                key, value = matched.groups()
                json[key] = value
            try:
                line = next(txt)
            except StopIteration:
                break
        
        for i in range(50):
            matched = re.match(r'Generation ([0-9]+) ', line)
            if matched:
                iteration, = matched.groups()
                json[iteration] = {}
            
            lines = next(txt).split('\n')
            assert lines[0] == 'Population: '
            json[iteration]['population'] = []
            for i in range(1, 31):
                json[iteration]['population'].append(eval(lines[i]))
            
            line = next(txt)

            matched = re.match(r'fitness: (\[(-[\d]+.[\d]+, )+-[\d]+.[\d]+\]) ', line)
            if matched:
                fitness, _ = matched.groups()
                json[iteration]['fitness'] = eval(fitness)

            try:
                txt2 = deepcopy(txt)
                lines = next(txt2).split('\n')
                
                assert lines[0] == "Better solution FOUND!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! "
                matched = re.match(r'best solution: (\(\[([\d]+, )+[\d]+\], -[\d]+.[\d]+\)) ', lines[1])
                if matched:
                    best_solution, _ = matched.groups()
                    best_solution, fitness = eval(best_solution)
                    json[iteration]['best_solution'] = {
                        'vector': best_solution,
                        'fitness': fitness
                    }

                line = next(txt)
            except AssertionError:...

            try:
                line = next(txt)
            except StopIteration:
                break

        s = ddb.at(f'test_{test}')
        if not s.exists():
            s.create(json)

        test += 1
