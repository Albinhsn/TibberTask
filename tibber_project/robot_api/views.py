from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt

from time import time
from datetime import datetime
from json import dumps, loads 

from utils import parse_body_from_request
from robot_api.utils import calculate_result, execution_insert_to_json
from robot_api.models import Execution 


@csrf_exempt #Remove if in prod
def enter_path(request):

    #Might need to change this if other request methods on same url needs to be implemented 
    if request.method != "POST":
        return HttpResponseNotFound("")
    
    #get content from body
    body = parse_body_from_request(request)

    #calculates the result 
    start_time = time() 
    result = calculate_result(body['start'], body['commands'])
    end_time =time() - start_time
    
    #insert into db
    exe = Execution.objects.create(
        timestamp=datetime.now(),
        commands=len(body['commands']),
        result=result,
        duration=end_time
    )

    #transform insert object into json response
    response = execution_insert_to_json(exe)

    #return record
    return JsonResponse(response) 


def get_all(request):
    objs = list(Execution.objects.values())
    for idx in range(len(objs)):
        objs[idx]['timestamp'] = objs[idx]['timestamp'].isoformat()
    objs = loads(dumps(objs))
    return JsonResponse(objs, safe=False)
