

from json import loads, dumps 


def calculate_result(start_pos, commands):
    x,y = start_pos['x'], start_pos['y']
    y_lines = {
        start_pos['x']: [
            {
                "low": start_pos['y'],
                "high": start_pos['y']
            }
        ]
    }
    x_lines = {
        start_pos['y']: [
            {
                "low": start_pos['x'],
                "high": start_pos['x']
            }
        ]
    }
    result = 0 
    for c in commands:
        if c['direction'] == "east":
            low = x
            high = x + c['steps']
            coord = y
            line = x_lines
            x = high
        elif c['direction'] == "west": 
            low = x - c['steps']
            high = x
            coord = y
            line = x_lines
            x = low
        elif c['direction'] == "north":
            low = y
            high = y + c['steps']
            coord = x
            line = y_lines
            y = high
        else:
            low = y - c['steps']
            high = y
            coord = x
            line = y_lines
            y = low 
            
        check_new_line(line, coord, low, high)
        print(x_lines, y_lines)
    
    for line in x_lines:  
        result += line['high'] - line['low']
        #TODO Remove times the intersect
    for line in y_lines:
        result += line['high'] - line['low']

    #TODO Figure out a way to calc results
    return result

def check_new_line(line, coord, low, high):
    #print(line, coord, low, high)
    if coord in line:
        if low >  line[coord][-1]['high']: 
            print("Appended it cos low above last high")
            line[coord].append({
                "low": low,
                "high": high
                })
            return 
        if high < line[coord][0]['low']:
            print("Inserted it at 0 cos high below first low ")
            line[coord].insert(0,{
                "low": low,
                "high": high
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
                    'high': high
                })
        #Line exists outside the bounds of current ones
        elif lowest == -1:
            #Line is lower
            if line[coord][0]['low'] > low:
                print("Inserted at 0")
                line[coord].insert(0, {
                    'low': low,
                    'high': high
                    })
            #Line is higher 
            else:
                print("Inserted in the back")
                line[coord].insert(len(line[coord]), {
                    'low': low,
                    'high': high
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
                    'high': high
                })
    #Line at coordinate didn't exist 
    else:
        line[coord] = [{
            "low": low,
            "high": high
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
