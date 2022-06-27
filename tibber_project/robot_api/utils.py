

from json import loads, dumps 
#TODO: Figure out way to improve speed and readability
def calculate_result(start_pos, commands):
    x,y = start_pos['x'], start_pos['y']
    y_lines = {}
    x_lines = {}
    start_points = {
            (x,y): 1
            }
    result = 1
    first = ""
    intersected = False
    if commands[0]['direction'] == "south" or commands[0]['direction'] == "north":
        y_lines[start_pos['x']] =[
            {
                "command": -1,
                "low": start_pos['y'],
                "high": start_pos['y']
            }
        ]
        first = "y"
    else:
        x_lines[start_pos['y']] = [
            {
                "command": -1,
                "low": start_pos['y'],
                "high": start_pos['y']
            }
        ]
    for idx, c in enumerate(commands):
        print( idx)
        if c['direction'] == "east":
            low = x
            high = x + c['steps']
            coord = y
            line = x_lines
            line_to_check = y_lines
            x = high
            axis = "x"
        elif c['direction'] == "west": 
            low = x - c['steps']
            high = x
            coord = y
            line = x_lines
            line_to_check = y_lines
            x = low
            axis = "x"
        elif c['direction'] == "north":
            low = y
            high = y + c['steps']
            coord = x
            line = y_lines
            line_to_check = x_lines
            y = high
            axis = "y"
        else:
            low = y - c['steps']
            high = y
            coord = x
            line = y_lines
            line_to_check = x_lines
            y = low 
            axis = "y"

        result -=  check_intersection(line_to_check, line, coord, low, high, idx, start_points, axis)
       
        check_new_line(line, coord, low, high, idx, c['direction'])
        if (x,y) not in start_points:
            start_points[(x,y)] = 1
    #    print(x_lines, y_lines)
        if first != axis and intersected == False:
           intersected = check_first_line_intersected(start_pos, coord, low, high, axis, idx, c['direction'], len(commands))
       # print_coordinates_visited(x_lines, y_lines)
    
   # print(f"result is {result} before calc cos {result* -1 +1} intersections")
    for x_key, x_val in x_lines.items():  
        
        for coord in x_val:
            result += get_difference_between_ints(coord['high'], coord['low'])    
      #      print(f"result = {result} after {coord} at x {x_key}")

    for key, line in y_lines.items():
        for coord in line:
            result += get_difference_between_ints(coord['high'], coord['low'])  
     #       print(f"result = {result} after {coord} at y {key}")
    #print(f"pre last_command {result}")
    #Check if last line intersected with smth
    last_command = commands[-1]['direction']
    if last_command  == "south":
        if check_intersection_last_line(x_lines, x, low, start_pos, axis):
            result -= 1
    elif last_command == "north":
        if check_intersection_last_line(x_lines, x, high, start_pos,axis):
            result -= 1
    elif last_command == "east":
        if check_intersection_last_line(y_lines, y, high, start_pos, axis):
            result -= 1
    else:
        if check_intersection_last_line(y_lines, y, low, start_pos, axis):
            result -= 1
   # print(f"after last_command {result}")
    return result



def check_first_line_intersected(start_pos, coord, low, high, axis, idx, direction, number_of_commands):
    if axis == "y":
        if coord == start_pos['x']:
            if high>start_pos['y']>low and idx != number_of_commands-1:
                return True
            if idx == number_of_commands-1:
                if direction == "north": 
                    if high>=to_check>low:
                        return True
                else:
                    if high>to_check>=low:
                        return True
    if axis == "x":
        if coord == start_pos['y']:
            if high>start_pos['x']>low and idx != number_of_commands-1:
                return True
            if idx == number_of_commands-1:
                if direction == "east": 
                    if high>=to_check>low:
                        return True
                else:
                    if high>to_check>=low:
                        return True
    return False


#Just checks if last lines high hits smth
def check_intersection_last_line(line, coord, high, start_pos, axis):
    print(f"last coord was {coord, high} or {high,coord}")
    #TODO Check if it has already hit this spot  
    #if coord in old_line:
     #   for i in old_line[coord]:
      #      if i['high']>=high>=i['low']:
       #         return False
    if high in line:
        #print(line[high], coord)
        for i in line[high]:
            if axis == "y":
                if i['high']>coord>i['low'] and (high, coord) != (start_pos['x'], start_pos['y']):
                    return True
            else:
                if i['high']>coord>i['low'] and (coord, high) != (start_pos['x'], start_pos['y']):
                    return True
    return False


def check_intersection(line, old_line, coord, low, high, idx, start_points, axis):
    count = 0
    for i in range(low, high+1):
        if i in line:
            for j in line[i]:
                #TODO: Check if needed to check idx +-1
#                print(f"j is {j}")
 #               print(f"coord is {coord}")
                if j['high']>=coord>=j['low'] and idx + 1 != j['command'] and idx -1 != j['command']:
                    if axis == "y":
                        if (coord, i) in start_points:
                            continue
                    else:
                        if (i, coord) in start_points:
                            continue
                    flag = False
                    for k in range(j['low']+2,j['high']):
                        if k in old_line:
  #                          print(old_line[k])
                            for z in old_line[k]:
                                if z['high']>=i>=z['low']:
                                    flag = True
                                    break
                    if not flag:
                        count += 1
   #                     print(f"found intersection at {j} and {coord}, {low}-{high}, {idx+1}")

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

def get_difference_between_ints(x, y): 
    if x>0 and y>0:
        return abs(y-x)
    return abs(x-y)
def check_new_line(line, coord, low, high, command_idx, direction):
    #print(line, coord, low, high)
    if coord in line:
        if low >  line[coord][-1]['high']: 
    #        print("Appended it cos low above last high")
            line[coord].append({
                "low": low,
                "high": high,
                "command": command_idx,
                "direction": direction
                })
            return 
        if high < line[coord][0]['low']:
     #       print("Inserted it at 0 cos high below first low ")
            line[coord].insert(0,{
                "low": low,
                "high": high,
                "command": command_idx,
                "direction": direction
                })
            return
        lowest, highest = -1, -1 
        for idx, l in enumerate(line[coord]): 
            if l['low'] > high:
                break
            if l['high'] > low or (high > l['low'] and l['high'] >= low):
                lowest = idx
                
            highest = idx
        #Line exists inbetween already existing ones
        if lowest == -1 and highest != len(line[coord])-1:
            line[coord].insert(highest+1, {
                    'low': low,
                    'high': high,
                    'command': command_idx,
                    "direction": direction
                })
        #Line exists outside the bounds of current ones
        elif lowest == -1:
            #Line is lower
            if line[coord][0]['low'] > low:
      #          print("Inserted at 0")
                line[coord].insert(0, {
                    'low': low,
                    'high': high,
                    'command': command_idx,
                    'direction': direction
                    })
            #Line is higher 
            else:
       #         print("Inserted in the back")
                line[coord].insert(len(line[coord]), {
                    'low': low,
                    'high': high,
                    "command": command_idx,
                    "direction": direction
                    }
                )
        #Line exists within already existing ones        
        else:
            if low > line[coord][lowest]['low']:
                low =  line[coord][lowest]['low']
            if high <  line[coord][highest]['high']:
                high =  line[coord][highest]['high']    
            highest += 1
            del line[coord][lowest:highest]
            line[coord].insert(lowest, {
                    'low': low,
                    'high': high,
                    'command': command_idx,
                    "direction": direction
                })
    #Line at coordinate didn't exist 
    else:
        line[coord] = [{
            "low": low,
            "high": high,
            "command": command_idx,
            "direction": direction
        }]
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
