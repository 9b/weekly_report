from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.template import RequestContext
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from pymongo import Connection

import os
import simplejson as json
import pymongo

from weekly_report.apps.util.views import connect_to_mongo
from weekly_report.apps.watchdog.views import check_report_date, is_auth

@csrf_exempt
def store_data(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		start_date = request.POST['startdt']
		end_date = request.POST['enddt']
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_tmp = start_date.split('/')
			end_tmp = end_date.split('/')
			key = start_tmp[0] + start_tmp[1] + start_tmp[2] + end_tmp[0] + end_tmp[1] + end_tmp[2]
			
			obj = { 'start_week':start_date, 'end_week':end_date, '_id':key }
			
			con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "meta")
			con.insert(obj)
			out['success'] = True
			out['start_date'] = start_date #TODO this should not sit in the root
			out['end_date'] = end_date #TODO this should not sit in the root
			out['id'] = key #TODO this should not sit in the root
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"
	

	
	