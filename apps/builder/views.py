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

from weekly_report.apps.util.views import connect_to_mysql, connect_to_mongo
from weekly_report.apps.watchdog.views import check_report_id, is_auth

@csrf_exempt
def build_report(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = request.POST['id']
		
		if check_report_id(key):
			# meta
			meta_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "meta")
			meta_data = meta_con.find_one({"_id":key},{"_id":0})
			
			# compromise counts
			counts_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_counts")
			compromise_counts_data = counts_con.find_one({"_id":key},{"_id":0})
		
			# compromise details
			compromise_details_data = []
			details_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_details")
			for item in details_con.find({"_id":key},{"_id":0}):
				rjson =  json.dumps(item)
				ruse = json.loads(rjson)
				details = ruse.get("details")
				if type(details) is not list:
					obj = { "ip_address": details.get("ip_address"), "compromise_notes": details.get("compromise_notes"), "key": details.get("key"), "original_notes": details.get("original_notes"), "school_department": details.get("school_department"), "time_of_compromise": details.get("time_of_compromise") }
					compromise_details_data.append(obj)
				else:
					for listing in details:
						compromise_details_data.append(listing)
					
		
			# compromise types
			compromise_types_data = []
			types_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_types")
			for item in types_con.find({"_id":key},{"_id":0}):
				rjson =  json.dumps(item)
				ruse = json.loads(rjson)
				details = ruse.get("details")
				if type(details) is not list:
					obj = { "name": details.get("name"), "value":details.get("value"), "key":details.get("key") }
					compromise_types_data.append(obj)		
				else:
					for listing in details:
						compromise_types_data.append(listing)	
					
			# average response time
			response_time_data = []
			response_time_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "average_response_time")
			for item in response_time_con.find({"_id":key},{"_id":0}):
				rjson =  json.dumps(item)
				ruse = json.loads(rjson)
				details = ruse.get("details")
				obj = { "name": details.get("name"), "value":details.get("value"), "key":details.get("key") }
				response_time_data.append(obj)	
					
			# historical data
			historical_compromise_data = []
			historical_con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "historical_compromises")
			for item in historical_con.find({"_id":key},{"_id":0}):
				rjson =  json.dumps(item)
				ruse = json.loads(rjson)
				details = ruse.get("details")
				for listing in details:
					historical_compromise_data.append(listing)
					
			# save the report
			con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
			obj = { "metadata": meta_data,
					"compromise_counts":compromise_counts_data,
					"compromise_details": { "compromise_listings":compromise_details_data, "summary_notes": "" },
					"compromise_types": { "type_listings":compromise_types_data, "summary_notes": "" },
					"historical_compromises": { "historical_listings":historical_compromise_data, "summary_notes": "" },
					"response_time":{ "average_response_time":response_time_data, "summary_notes": "" }
			}
			
			final = { "_id":key, "report": obj }
			con.insert(final)
			
			# kill temp storage
			meta_con.remove()
			counts_con.remove()
			details_con.remove()
			types_con.remove()
			historical_con.remove()
			response_time_con.remove()
			
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Warning: mysql_fetch_array(): supplied argument is not a valid MySQL result resource in /var/www/production/build_report.php on line 168"
			return render_to_response("error.html",out,context_instance=RequestContext(request))	
	
def fetch_report(request,rid,template_name):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	reports = []
	
	if is_auth(request):
		if check_report_id(rid):
			con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
			data = con.find_one({"_id":rid},{"report.metadata":1})
			rjson =  json.dumps(data)
			ruse = json.loads(rjson)
			report = ruse.get("report")
			metadata = report.get("metadata")
			start_date = metadata.get("start_week")
			end_date = metadata.get("end_week")
			obj = { "start_date":start_date,"end_date":end_date }
		
			out['results'] = obj
			out['success'] = True
			return render_to_response(template_name,out,context_instance=RequestContext(request))
		else:
			out['error'] = "Warning: mysql_query() [function.mysql-query]: Unable to save result set in /var/www/production/save.php on line 29"
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		return render_to_response('login.html',out,context_instance=RequestContext(request))