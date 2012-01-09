from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.core.urlresolvers import reverse
from django.core.context_processors import csrf
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder
from django.utils import simplejson
from pymongo import Connection
from weekly_report.apps.watchdog.views import is_auth

import os
import simplejson as json
import pymongo
import MySQLdb
import sys

def connect_to_mongo(host, port, database, collection):
	connection = Connection(host, port)
	db = connection[database]
	collection = db[collection]
	return collection
	
def connect_to_mysql(host, user, password, database):
    out = { 'results':{},'error':{},'session':{}, 'success': False }
    try:
        conn = MySQLdb.connect (host, user, password, database)
        return conn
    except MySQLdb.Error, e:
        out['error'] = "Error %d: %s" % (e.args[0], e.args[1])
        
def kill_mysql_connection(conn):
    conn.commit()
    conn.close()
    
def created_reports(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	reports = []
	
	if is_auth(request):
		con = connect_to_mongo('127.0.0.1',27017, "weekly_report", "complete_reports")
		for report in con.find({},{"report.metadata":1}):
			rjson =  json.dumps(report)
			ruse = json.loads(rjson)
			id = ruse.get("_id")
			report = ruse.get("report")
			metadata = report.get("metadata")
			start_date = metadata.get("start_week")
			end_date = metadata.get("end_week")
			obj = { "id":id,"start_date":start_date,"end_date":end_date }
			reports.append(obj)
			
		out['results'] = reports
		out['success'] = True
		return render_to_response('main.html',out,context_instance=RequestContext(request))
	else:
		return render_to_response('login.html',out,context_instance=RequestContext(request))
		
def generate_report(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	if is_auth(request,True):
		return render_to_response('generate.html',out,context_instance=RequestContext(request))
	else:
		out['error'] = "Access denied"
		return render_to_response('error.html',out,context_instance=RequestContext(request))
	
def captured_login(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	return render_to_response('login.html',out,context_instance=RequestContext(request))
	
def handle_error(request):
	out = { 'results':{},'error':{},'session':{},'login':{} }
	out['error'] = "The page you request doesn't exist"
	return render_to_response('error.html',out, context_instance=RequestContext(request))