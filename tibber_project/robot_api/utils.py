

from json import loads, dumps
from re import I
def calculate_result(start_pos, commands):
    if len(commands) == 0:
        return 1 
    #Lines are stored with position on the other axis as key, then a list of tuples containing the lowest and highest point on the line      
    x_lines = {}
    x_keys = []

    y_lines = {}
    y_keys = []
    
    x,y = start_pos['x'], start_pos['y']
    result = 0  
    
    #Iterate over the given commands
    #Calculate the position, the low and high points and the axis of the new line
    for command in commands:
        x,y, low, high, axis = create_new_line(x,y, command) 
        #Add the new line and calculate the amount of new points it creates on the same axis
        if axis == "y":
            result += add_new_line(y_lines, low, high, x, command['steps'], y_keys)                            
        else:
            result += add_new_line(x_lines, low, high, y, command['steps'], x_keys)
    #Calculate and remove the number of intersections between the axes 
    result -= check_intersection(x_lines, y_lines, x_keys, y_keys)    
    return result

#Takes in current position and the command
#Returns the new position, the low and high of the new line and the axis for it
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



#Checks how many times the lines on the different axes intersected 
#Returns the number of intersections
def check_intersection(x_lines, y_lines, x_keys, y_keys):
    intersections = 0
    for xkey in x_keys:
        for x_line in x_lines[xkey]:
            for y_key in [y_key for y_key in y_keys if x_line[1]>=y_key>=x_line[0]]:
                for y_line in y_lines[y_key]:
                    if y_line[1]>=xkey>=y_line[0]:                    
                        intersections += 1
                        break
    return intersections

#Adds or inserts a new line to the lines
#Also adds a new key to keys if present
#Returns back the number of new points 
def add_new_line(lines, low, high, key, steps, keys):
    result = steps + 1 
    if key in lines:
        #Line exist above every other line
        if low>lines[key][-1][1]:
            lines[key].append((low,high))
        #Line exist below every other line
        elif high<lines[key][0][0]:
            lines[key].insert(0, (low,high))
        #Line exist inbetween or inside existing ones
        else:  
            #Iterate over current lines to find location of the new line
            low_idx, high_idx, prev_count = 0,0,0            
            for line_idx, line in enumerate(lines[key]):
                if line[0]>high:
                    break
                if low>line[1]:
                    low_idx = line_idx + 1
                    continue
                prev_count += abs(line[1]- line[0]) + 1
                high_idx = line_idx 
            
            #Assigns low and high for the new line
            if lines[key][low_idx][0]<low:
                low = lines[key][low_idx][0]
            if lines[key][high_idx][1]>high:
                high = lines[key][high_idx][1]
            
            #Deletes the previous lines and inserts the combined one
            del lines[key][low_idx:high_idx+1]
            lines[key].insert(low_idx, (low,high))
            #Count is difference between the length of the new line and result of points from the previous line
            result = abs(high-low) + 1 - prev_count
    #No Lines existed on the given key 
    else:
        lines[key] = [(low,high)]        
        keys.append(key)
    return result  

#Reformats Execution object
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
