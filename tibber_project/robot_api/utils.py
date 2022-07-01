

from json import loads, dumps
from re import I 
def calculate_result(start_pos, commands):
    x_lines = {

    }
    y_lines = {

    }
    x,y = start_pos['x'], start_pos['y']
    count = 0
    
    for command in commands:
        x,y, low, high, axis = create_new_line(x,y, command) 
        if axis == "y":
            count += add_new_line(y_lines, low, high, x, command['steps'])        
        else:
            count += add_new_line(x_lines, low, high, y, command['steps'])
    count -= check_intersection(x_lines, y_lines)    
    return count
def create_new_line(x,y, command):
    if command['direction'] == "north":
        axis = "y"
        low = y
        y += command['steps']
        high = y 
    elif command['direction'] == "south":
        axis = "y"
        high = y 
        y -= command['steps']
        low = y 
    elif command['direction'] == "east":
        axis = "x"
        low = x 
        x += command['steps']
        high = x
    else:
        axis = "x"
        high = x        
        x -= command['steps']
        low = x         
    return x,y,low, high, axis
def print_coordinates_visited(x, y):
    s = set()
    for i in x: 
        for j in x[i]:
            s.update([(k,i) for k in range(j['low'], j['high']+1)])
    for i in y:
        for j in y[i]:
            s.update([(i,k) for k in range(j['low'], j['high']+1)])
    return len(s)


def check_intersection(x_lines, y_lines):    
    intersections = 0
    for key,val in x_lines.items():
        for i in val:
            for j in range(i['low'], i['high']+1):
                if j in y_lines:
                    for k in y_lines[j]:
                        if k['high']>=key>=k['low']:
                            intersections += 1                            
                            break            
    return intersections

def add_new_line(line, low, high, p, steps):
    count = steps + 1 
    if p in line:
        if low>line[p][-1]['high']:
            line[p].append({'low': low, 'high': high})
        elif high<line[p][0]['low']:
            line[p].insert(0, {'low': low, 'high': high})
        else:  
            l, h,prev_count = 0,0,0
            for idx, val in enumerate(line[p]):
                if val['low']>high:
                    break
                if low>val['high']:
                    l = idx + 1
                    continue
                if val['high']>=high and val['low']<=low:
                    return 0
                prev_count += abs(val['high']- val['low']) + 1
                h = idx
            
            if line[p][l]['low']<low:
                low = line[p][l]['low']
            if line[p][h]['high']>high:
                high = line[p][h]['high']
            del line[p][l:h+1]
            line[p].insert(l, {'low': low, 'high': high})
            count = abs(high-low) + 1 - prev_count
    else:
        line[p] = [{'low': low, 'high': high}]        
    return count  
def execution_insert_to_json(exe):
    #transform execution object into dict
    exe = exe.__dict__

    #Remove state key
    if '_state' in exe:
        del exe['_state']
    
    #Changes datetime to string format 
    exe['timestamp'] = str(exe['timestamp'])
    
    #Changes duration from scientific notation (1e^-5) to decimal
    exe['duration'] = "{:f}".format(exe['duration'])

    #Returns in json format
    return loads(dumps(exe))
