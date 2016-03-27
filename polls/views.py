from django.shortcuts import render
from django.http import HttpResponse

import commands
import json
import os

def index(request):
	return render(request, 'index.html')

def pull(request):
	if request.method == 'GET':
		file_path = request.GET.get('file_path')
		if not file_path or len(file_path)==0:
			return HttpResponse('illegal file_path parameter')
		if not os.path.exists(file_path):
			return HttpResponse('file path: ' + file_path + ' does not exists, pls check!')
		if not os.path.isfile(file_path):
			return HttpResponse('file path: ' + file_path + ' is not file, pls check!')
		begin = request.GET.get('begin', 1)
		offset = request.GET.get('offset', 10)
		cmd = "sed -n '{0},{1}p' {2}".format(str(begin), str(begin + offset), file_path)
		result = commands.getstatusoutput(cmd)
		content = result[1]
		response_data = {}
		if content:
			response_data['data'] = content.splitlines()
			response_data['length'] = len(response_data['data'])
		else:
			response_data['length'] = 0
			
		return HttpResponse(json.dumps(response_data), content_type="application/json")
	else:
		return HttpResponse('illegal http method')
