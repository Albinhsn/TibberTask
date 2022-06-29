

from json import loads, dumps 
def calculate_result(start_pos, commands):
    #Create current pos with x,y 
    x_lines = {

    }
    y_lines = {

    }
    prev_axis = ""
    current_position = start_pos['x'], start_pos['y']
    count = 1
    if commands[0]['direction'] == "north" or commands[0]['direction'] == "south":
        y_lines[start_pos['x']] = [{'low': start_pos['y'], 'high': start_pos['y']}]
    else:
        x_lines[start_pos['y']] = [{'low': start_pos['x'], 'high': start_pos['x']}]
    #Create start pos with XX and YY 
    for idx, command in enumerate(commands):
    #Create new line depending on direction
        print("-----------")
        print(f"command: {idx+1} direction is {command['direction']} and steps is {command['steps']}")
        current_position, low, high, axis = create_new_line(current_position, command) 
    #Check if new line intersects with smth on the other axis
        if axis == "y":
            count -= check_intersection(x_lines, y_lines, low, high, current_position[0], command['direction'])
        else:
            count -= check_intersection(y_lines, x_lines, low, high, current_position[1], command['direction'])
        
    #Add new line and add the difference of steps to count
        prev = count
        if axis == "y":
            count += add_new_line(y_lines, low, high, current_position[0], command['direction'], axis, prev_axis)
        else:
            count += add_new_line(x_lines, low, high, current_position[1], command['direction'],axis, prev_axis)
        print(f"added {count-prev}. Count is:{count}")
        #print_coordinates_visited(x_lines, y_lines)
        prev_axis = axis
    return count
#Gets tuple of x,y and current command
#Returns new x,y, high, low and axis
def create_new_line(current_position, command):
    if command['direction'] == "north":
        axis = "y"
        low = current_position[1]
        high = current_position[1] + command['steps']
        current_position = (current_position[0],current_position[1]+command['steps'])
    elif command['direction'] == "south":
        axis = "y"
        low = current_position[1] - command['steps']
        high = current_position[1] 
        current_position = (current_position[0],current_position[1]-command['steps'])
    elif command['direction'] == "east":
        axis = "x"
        low = current_position[0] 
        high = current_position[0]+ command['steps']
        current_position = (current_position[0]+command['steps'],current_position[1])
    #Direction is west
    else:
        axis = "x"
        low = current_position[0] - command['steps']
        high = current_position[0]        
        current_position = (current_position[0]-command['steps'],current_position[1])

        
    return current_position, low, high, axis



#TODO: Figure out better name for 'p'
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
                    #TODO: If lines first point hits smth, don't let it
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
    print(f"found {intersections} intersections")
    if direction == "north" or direction == "east":
        low -= 1 
    else:
        high += 1
    return intersections
#Adds new line to lines
#Returns number of points added
def add_new_line(line, low, high, p, direction, axis, prev_axis):
    count = abs(high-low) 
    print(f"add_new_line count is {count}")
    if p in line:
        #Line exis after all existing lines
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
                    continue
                if val['high']>=low>=val['low']:
                    l = idx
                if val['high']<high and low<val['low']:
                    prev_count += 1 
                prev_count += abs(val['high']- val['low']) 
                h = idx
            print(f"found {prev_count} in prev at {line[p]}, with p:{p}, low:{low}, high:{high}")
            #TODO: When a new line gets added on the same axis and its coming from "outside and in" and doesn't go through but stops inbetween. Count needs to be reduced by one cos otherwise abs(low-high) gets scuffed
            flag = False
            print(f"low: {low}, pllow: {line[p][l]['low']}, high: {high}, phhigh: {line[p][h]['high']}, direction: {direction}")
            if high<=line[p][h]['high']:
                if direction == "north" or direction == "east":
                    print("FLAG 1")
                    flag = True
            if low>=line[p][l]['low']:
                if direction == "south" or direction == "west":
                    print("FLAG 2 ")
                    flag = True

            if line[p][l]['low']<low:
                low = line[p][l]['low']
            
            if line[p][h]['high']>high:
                high = line[p][h]['high']
            del line[p][l:h+1]
            line[p].insert(l, {'low': low, 'high': high})
            
            count = abs(high-low) - prev_count
            if flag and count > 0:
                print("FLAGGERINO")
                count -= 1

            print(f"count became {count} from h:{high}, l:{low} and prev:{prev_count}")
    else:
        line[p] = [{'low': low, 'high': high}]
    print(f"returning add_new_line count as {count}")
    return count
def print_coordinates_visited(x, y):
    s = set()
    for i in x: 
        for j in x[i]:
            if j['low'] == j['high']:
                continue
            for k in range(j['low'], j['high']+1):
                
                s.add((k, i))
    for i in y:
        for j in y[i]:
            if j['low'] == j['high']:
                continue
            for k in range(j['low'], j['high']+1):
                s.add((i,k))
    print(s)
    #print(f"result should be {len(s)}")

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
