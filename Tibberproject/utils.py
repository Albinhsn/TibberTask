



from json import loads
from time import time
#Calculates the result of path
#Returns result and duration of calculation 
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

def parse_body_from_request(request):
    #https://stackoverflow.com/questions/29780060/trying-to-parse-request-body-from-post-in-django
    body_unicode = request.body.decode('utf-8')
    body = loads(body_unicode)
    ##Might need to change this to include content
    return body
