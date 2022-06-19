

from json import loads, dumps 


def calculate_result(start_pos, commands):

    current_pos = (start_pos['x'], start_pos['y'])
    unique_positions = set()
    unique_positions.add(current_pos)

    #Iterate over commands
    for command in commands: 
        if command['direction'] == "east":
            direction = (1, 0)
        elif command['direction'] == "west":
            direction = (-1, 0)
        elif command['direction'] == "north":
            direction = (0, 1)
        else:
            #Direction is south
            direction = (0, -1)
        #Calcing every step
        for _ in range(command['steps']):

            current_pos = tuple(map(lambda i, j: i - j, current_pos, direction))
            unique_positions.add(current_pos)
    return len(unique_positions)



def execution_insert_to_json(exe):
    #transform execution object into dict
    exe = exe.__dict__

    #Remove state key
    if '_state' in exe:
        del exe['_state']

    #Changes from date format to iso, will break json serializer if removed
    if 'timestamp' in exe:
        exe['timestamp']=exe['timestamp'].isoformat()
    #Changes duration from scientific notation (1e^-5) to decimal
    exe['duration'] = "{:f}".format(exe['duration'])

    #Returns in json format
    return loads(dumps(exe))
