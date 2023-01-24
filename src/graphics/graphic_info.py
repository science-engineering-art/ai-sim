import dictdatabase as ddb
from sys import maxsize as oo


def get_graphic_info():
    info = { }

    for i in range(50):
        json = ddb.at(f'test_{i}').read()
        
        i = str(i)
        info[i] = { 'mins': [], 'maxs': [] }

        for j, iter in json['iterations'].items():
            
            k, min = 0,  oo
            h, max = 0, -oo

            for g, fit in enumerate(iter['fitness']):
                if fit > max:
                    h, max = g, fit
                if fit < min:
                    k, min = g, fit

            info[i]['mins'].append((min, int(j), k))
            info[i]['maxs'].append((max, int(j), h))

    return info
