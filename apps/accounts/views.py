from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.auth import logout

import ldap
import getpass
import hashlib
import random
import string

@csrf_exempt
def ext_login(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
    
	# debug
	#ldap.set_option(ldap.OPT_DEBUG_LEVEL,4095)

	# config
	ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
	ldap.set_option(ldap.OPT_X_TLS_CACERTFILE,"/var/www/weekly_report/media/auth/gwu.crt")
	l = ldap.initialize(settings.LDAP_SERVER)
	l.set_option(ldap.OPT_PROTOCOL_VERSION, 3)

	# defined - no need to watchdog these given they are going to LDAP for a bind
	netid = request.POST['netid'] 
	pw = request.POST['password']
	dn = "uid=" + netid + ",ou=people,dc=gwu,dc=edu"
	
	try:
		l.simple_bind_s(dn,pw)
		out['success'] = True
		request.session.set_expiry(300)
		request.session['logged'] = hashlib.sha224(netid + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))).hexdigest()
		if netid == "bsdixon" or netid == "mwollenw" or netid == "sechigh":
			request.session['admin'] = hashlib.sha224(dn + ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(10))).hexdigest()
	except ldap.LDAPError as error_message:
		out['error'] = "Credentials not valid"	
	
	return HttpResponse(simplejson.dumps(out, cls=DjangoJSONEncoder))

def logout_user(request):
	out = { 'results':{},'error':{},'session':{}, 'success': False }
	logout(request)
	return render_to_response('login.html',out,context_instance=RequestContext(request))