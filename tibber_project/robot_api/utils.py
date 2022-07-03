

from json import loads, dumps
def calculate_result(start_pos, commands):
    if len(commands) == 0:
        return 1  
    x_lines = {}
    y_lines = {}
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
            for j in [y for y in y_lines.keys() if i[1]>=y>=i[0]]:
                    for k in y_lines[j]:
                        if k[1]>=key>=k[0]:
                            intersections += 1                            
                            break 
    return intersections

def add_new_line(line, low, high, p, steps):
    count = steps + 1 
    if p in line:
        if low>line[p][-1][1]:
            line[p].append((low,high))
        elif high<line[p][0][0]:
            line[p].insert(0, (low,high))
        else:  
            l, h,prev_count = 0,0,0
            for idx, val in enumerate(line[p]):
                if val[0]>high:
                    break
                if low>val[1]:
                    l = idx + 1
                    continue
                prev_count += abs(val[1]- val[0]) + 1
                h = idx 
            
            if line[p][l][0]<low:
                low = line[p][l][0]
            if line[p][h][1]>high:
                high = line[p][h][1]
            del line[p][l:h+1]
            line[p].insert(l, (low,high))
            count = abs(high-low) + 1 - prev_count
    else:
        line[p] = [(low,high)]        
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
