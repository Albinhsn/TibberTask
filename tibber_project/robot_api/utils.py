

from json import loads, dumps 
def calculate_result(start_pos, commands):
    #Create current pos with x,y 
    x_lines = {

    }
    y_lines = {

    }
    x,y = start_pos['x'], start_pos['y']
    count = 1
    if commands[0]['direction'] == "north" or commands[0]['direction'] == "south":
        y_lines[x] = [{'low': y, 'high': y}]
    else:
        x_lines[y] = [{'low': x, 'high': x}]
    #Create start pos with XX and YY 
    for command in commands:
    #Create new line depending on direction
        x,y, low, high, axis = create_new_line(x,y, command) 
    #Check if new line intersects with smth on the other axis
        if axis == "y":
            count -= check_intersection(x_lines, y_lines, low, high, x, command['direction'])
        else:
            count -= check_intersection(y_lines, x_lines, low, high, y, command['direction'])
        
    #Add new line and add the difference of steps to count
        if axis == "y":
            count += add_new_line(y_lines, low, high, x, command['direction'])
        else:
            count += add_new_line(x_lines, low, high, y, command['direction'])
    return count
#Gets tuple of x,y and current command
#Returns new x,y, high, low and axis
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
    #Direction is west
    else:
        axis = "x"
        high = x        
        x -= command['steps']
        low = x         
    return x,y,low, high, axis



#Checks if new line intersects with something on the other axis, if yes check if it already exists on the same axis
#Returns the amount of times the line intersects 
def check_intersection(line_to_check, same_line, low, high, p, direction):
    
    intersections = 0
    if direction == "north" or direction == "east":
        low += 1
    else:
        high -= 1
    for i in range(low, high+1):
        if i in line_to_check:
            for line in line_to_check[i]:
                if line['high']>=p>=line['low']:
                    #Found intersection on other axis
                    if p in same_line:
                        flag = False
                        for j in same_line[p]:
                            if j['high']>=i>=j['low']:
                                flag = True
                                break
                        if flag:
                            continue
                    intersections += 1
    if direction == "north" or direction == "east":
        low -= 1 
    else:
        high += 1
    return intersections



#Adds new line to lines
#Returns number of points added
def add_new_line(line, low, high, p, direction):
    count = abs(high-low) 
    #print(f"add_new_line count is {count}")
    if p in line:
        #Line exis after all existing lines
        if low>line[p][-1]['high']:
            line[p].append({'low': low, 'high': high})
            
        elif high<line[p][0]['low']:
            line[p].insert(0, {'low': low, 'high': high})
        #Line overlaps another or is inbetween two
        else:  
            l, h,prev_count = 0,0,0
            for idx, val in enumerate(line[p]):
                if val['low']>high:
                    break
                if low>val['high']:
                    l = idx + 1
                    continue
                if val['high']<high and low<val['low']:
                    prev_count += 1 
                prev_count += abs(val['high']- val['low']) 
                h = idx
            #TODO: If l>: insert return count 
            #Line is inbetween two lines
            
            #Line overlaps with 1 other
            flag = False
            if high<=line[p][h]['high']:
                if direction == "north" or direction == "east":
                    flag = True
            if low>=line[p][l]['low']:
                if direction == "south" or direction == "west":
                    flag = True
            
            #Calculate new low
            if line[p][l]['low']<low:
                low = line[p][l]['low']
            #Calculate new high
            if line[p][h]['high']>high:
                high = line[p][h]['high']
            #Remove old line and insert new one
            del line[p][l:h+1]
            line[p].insert(l, {'low': low, 'high': high})
            #count is difference between new line and old line(s)
            count = abs(high-low) - prev_count
            if flag and count > 0:
                count -= 1
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
