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
from weekly_report.apps.watchdog.views import check_report_date, check_report_id, is_auth

# DRAFTING QUERIES

def get_compromise_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1]
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
			cursor = con.cursor ()
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category > 1" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			total_count = row[0]
			
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category = 20" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			student_count = row[0]
			
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category >= 100" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			normal_count = row[0]
			
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category > 200" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			vip_count = row[0]
			
			tmp = { 'total_count':total_count, 
					'student_count':student_count,
					'staff_faculty_count':normal_count,
					'patchlink_count':0,
					'non_patchlink_count':0,
					'email_count':0,
					'key':key
			}
			
			out['results'] = tmp
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"
	
def get_compromise_details(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		objs = []
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1]
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
			cursor = con.cursor ()
			stmt = "SELECT INET_NTOA(victim) as victim, network, discovered, notes FROM gwcases WHERE (report_category >= 100) AND DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' GROUP BY victim ORDER BY tdstamp, victim"
			cursor.execute(stmt)
			result_set = cursor.fetchall ()
			for row in result_set:
				obj = { 
					'ip_address':str(row[0]), 
					'school_department':str(row[1]),
					'time_of_compromise':str(row[2]),
					'compromise_notes':str(row[3]),
					'original_notes':str(row[3]),
					'key':key 
				}
				objs.append(obj)
				
			out['results'] = objs
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)	
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"
		
def get_average_response_time_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1]
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
			cursor = con.cursor ()
			stmt = "select AVG(TIME_TO_SEC(TIMEDIFF(tdstamp, discovered))) * 0.000277777778 as delta from gwcases where date(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category > 1 AND TIME_TO_SEC(TIMEDIFF(tdstamp,discovered)) > 0" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			avg_resp = round(row[0],2)
			
			tmp = { 'name':"Average Response",
					'value':str(avg_resp), 
					'key':key
			}
			
			out['results'] = tmp
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"
	
def get_normal_graph_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		objs = []
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1]
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
			cursor = con.cursor ()
			
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category = 20" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			student_count = row[0]
			
			stmt = "SELECT COUNT(*) as count FROM gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category >= 100" 
			cursor.execute(stmt)
			row = cursor.fetchone()
			normal_count = row[0]
			
			obj = { 'name':'Faculty/Staff','value':normal_count,'key':key }
			objs.append(obj)
			obj = { 'name':'Student','value':student_count,'key':key }
			objs.append(obj)
				
			out['results'] = objs
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))	
	else:
		while True:
			die = "slowly"
	
def get_compromise_types(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		objs = []
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1]
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
			cursor = con.cursor ()
			
			stmt = "select primary_detection, count(*) as count from gwcases WHERE DATE(tdstamp) BETWEEN '" + start_date + "' AND '" + end_date + "' AND report_category > 0 and report_category != 42 and primary_detection != '' group by primary_detection" 
			cursor.execute(stmt)
			result_set = cursor.fetchall ()
			for row in result_set:
				obj = { 
					'name':str(row[0]), 
					'value':int(row[1]),
					'key':key
				}
				objs.append(obj)
				
			out['results'] = objs
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"	
	
def get_historical_compromises(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		objs = []
		start_date = request.GET.get('start_date')
		end_date = request.GET.get('end_date')
		
		if check_report_date(start_date) and check_report_date(end_date):
			start_parts = start_date.split("/")
			end_parts = end_date.split("/")
			start_date = start_parts[2] + "-" + start_parts[0]  + "-" + start_parts[1] #year-month-day
			end_date = end_parts[2] + "-" + end_parts[0]  + "-" + end_parts[1]
			key = start_parts[0] + start_parts[1] + start_parts[2] + end_parts[0] + end_parts[1] + end_parts[2]
			
			import datetime
			from datetime import timedelta
			
			s = datetime.date(int(start_parts[2]),int(start_parts[0].lstrip('0')),int(start_parts[1].lstrip('0')))
			e = datetime.date(int(end_parts[2]),int(end_parts[0].lstrip('0')),int(end_parts[1].lstrip('0')))
		
			for n in range((e - s).days +1):
				cur_d = s + timedelta(n)
				current_date = cur_d.strftime("%Y-%m-%d")
			
				con = connect_to_mysql("128.164.80.81","dragonslayer","slayer","dragonslayer")
				cursor = con.cursor ()
			
				stmt = "SELECT COUNT(id) as c, date(tdstamp) as d from gwcases where DATE(tdstamp) = '" + current_date + "' AND (report_category > 42 OR report_category = 20) AND (report_category != 205 AND report_category != 25) group by day(tdstamp) ORDER BY id, day(tdstamp)"
				cursor.execute(stmt)
				row = cursor.fetchone()
				if row != None:
					current_count = row[0]
				else:
					current_count = 0
					
				pre_d = s + timedelta(n) - timedelta(days=365)
		 		previous_date = pre_d.strftime("%Y-%m-%d")
				stmt = "SELECT COUNT(id) as c, date(tdstamp) as d from gwcases where DATE(tdstamp) = '" + previous_date + "' AND (report_category > 42 OR report_category = 20) AND (report_category != 205 AND report_category != 25) group by day(tdstamp) ORDER BY id, day(tdstamp)"
				cursor.execute(stmt)
				row = cursor.fetchone()
				if row != None:
					previous_count = row[0]
				else:
					previous_count = 0
		
				obj = { 
					'current_year':str(cur_d.strftime("%Y")), 
					'previous_year':str(pre_d.strftime("%Y")),
					'current_count':int(current_count),
					'previous_count':int(previous_count),
					'date':str(cur_d.strftime("%m/%d")),
					'key':key
				}
				objs.append(obj)
				
			out['results'] = objs
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)
		else:
			out['error'] = "Attempting to travel time with the dates you supplied. Check back last week."
			return render_to_response("error.html",out,context_instance=RequestContext(request))	
	else:
		while True:
			die = "slowly"
	
@csrf_exempt
def set_compromise_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		obj = json.loads(request.raw_post_data)
		key = None
		try:
			obj['_id'] = obj.get("key")
			con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_counts")
			con.insert(obj)
			
			out['success'] = True
			mimetype = 'application/javascript'
			return HttpResponse(json.dumps(out),mimetype)	
		except:
			out['error'] = "Data blob failed to pass inspection."
			return render_to_response("error.html",out,context_instance=RequestContext(request))
	else:
		while True:
			die = "slowly"		
	
@csrf_exempt
def set_compromise_details(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = None
		objs = json.loads(request.raw_post_data)
		try:
			for o in objs:
				key = o.get("key")
		except:
			key = objs.get("key")
			
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_details")
		obj = { "_id": key, "details": objs }
		con.insert(obj)
		
		out['success'] = True
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)	
	else:
		while True:
			die = "slowly"
	
@csrf_exempt
def set_average_response_times(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = None
		objs = json.loads(request.raw_post_data)
		key = objs.get("key")
			
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "average_response_time")
		obj = { "_id": key, "details": objs }
		con.insert(obj)
		
		out['success'] = True
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		while True:
			die = "slowly"	
	
@csrf_exempt
def set_normal_graph_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = None
		objs = json.loads(request.raw_post_data)
		try:
			for o in objs:
				key = o.get("key")
		except:
			key = objs.get("key")
			
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "normal_graph_counts")
		obj = { "_id": key, "details": objs }
		con.insert(obj)
		
		out['success'] = True
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		while True:
			die = "slowly"
	
@csrf_exempt
def set_compromise_types(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = None
		objs = json.loads(request.raw_post_data)
		try:
			for o in objs:
				key = o.get("key")
		except:
			key = objs.get("key")
			
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "compromise_types")
		obj = { "_id": key, "details": objs }
		con.insert(obj)
		
		out['success'] = True
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)	
	else:
		while True:
			die = "slowly"
	
@csrf_exempt
def set_historical_compromises(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	
	if is_auth(request,True):
		key = None
		objs = json.loads(request.raw_post_data)
		try:
			for o in objs:
				key = o.get("key")
		except:
			key = objs.get("key")
			
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "historical_compromises")
		obj = { "_id": key, "details": objs }
		con.insert(obj)
		
		out['success'] = True
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		while True:
			die = "slowly"
	
def get_stored_compromise_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.compromise_counts":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		compromise_counts = report.get("compromise_counts")
		out['success'] = True
		out['compromise_counts'] = compromise_counts
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))
	
def get_stored_compromise_details(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.compromise_details.compromise_listings":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		compromise_details = report.get("compromise_details")
		compromise_listings = compromise_details.get("compromise_listings")
		out['success'] = True
		out['compromise_details'] = compromise_listings
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))	
		
def get_stored_average_response_time(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.response_time":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		response_time = report.get("response_time")
		average_response_time = response_time.get("average_response_time")
		out['success'] = True
		out['results'] = average_response_time
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))
	
def get_stored_normal_counts(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		tmp = []
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.compromise_counts":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		compromise_counts = report.get("compromise_counts")
		normal = compromise_counts.get("staff_faculty_count")
		student = compromise_counts.get("student_count")
		obj = {"name":"Faculty/Staff","value":normal}
		tmp.append(obj)
		obj = {"name":"Student","value":student}
		tmp.append(obj)
		out['success'] = True
		out['results'] = tmp
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))	
	
def get_stored_compromise_types(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.compromise_types.type_listings":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		compromise_types = report.get("compromise_types")
		type_listings = compromise_types.get("type_listings")
		out['success'] = True
		out['type_listings'] = type_listings
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))	
	
def get_stored_historical_compromises(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
	key = None
	key = str(request.GET['key'])
	if check_report_id(key):
		key = str(request.GET['key'])
		data = con.find_one({"_id":key},{"report.historical_compromises.historical_listings":1,"_id":0})
		rjson =  json.dumps(data)
		ruse = json.loads(rjson)
		report = ruse.get("report")
		historical_compromises = report.get("historical_compromises")
		historical_listings = historical_compromises.get("historical_listings")
		out['success'] = True
		out['historical_listings'] = historical_listings
		mimetype = 'application/javascript'
		return HttpResponse(json.dumps(out),mimetype)	
	else:
		out['success'] = False
		out['error'] = "Invalid key in request."
		return render_to_response("error.html",out,context_instance=RequestContext(request))		