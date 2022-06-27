

from json import loads, dumps 


def calculate_result(start_pos, commands):

    x,y = start_pos['x'], start_pos['y']
    unique_positions = set()

    #Iterate over commands
    for idx, command in enumerate(commands): 
        if command['direction'] == "east":
            new_pos = [(x+i,y) for i in range(command['steps']+1)]
            x += command['steps']
        elif command['direction'] == "west":
            new_pos = [(x-i,y) for i in range(command['steps']+1)]
            x -=  command['steps'] 
        elif command['direction'] == "north":
            new_pos = [(x,y+i) for i in range(command['steps']+1)]
            y += command['steps']
        else:
            #Direction is south
            new_pos = [(x,y-i) for i in range(1,command['steps']+1)]
            y -= command['steps']
        #Add every new pos to set
        unique_positions.update(new_pos)
    
        print(idx)
    return len(unique_positions)



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
