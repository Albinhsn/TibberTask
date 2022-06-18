from django.shortcuts import render

# Create your views here.

from django.http import JsonResponse, HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from utils import calculate_result, parse_body_from_request
from time import time
from datetime import datetime
from robot_api.models import Execution 
from json import dumps, loads 

@csrf_exempt
def enter_path(request):
    if request.method != "POST":
        return HttpResponseNotFound("")
    #get content from body
    body = parse_body_from_request(request)

    #calc result 
    start_time = time() 
    result = calculate_result(body['start'], body['commands'])
    #Changes from scientific format to decimal 
    end_time ="{:f}".format(time() - start_time)
    
    #insert into db
    exe = Execution.objects.create(
        timestamp=datetime.now(),
        commands=len(body['commands']),
        result=result,
        duration=end_time
    )
    
    #Transform object into dict
    exe = exe.__dict__
    del exe['_state']
    exe['timestamp'] = exe['timestamp'].isoformat()
    
    #Transform dict into json 
    exe = loads(dumps(exe))

    #return record
    return JsonResponse(exe, safe=False)
