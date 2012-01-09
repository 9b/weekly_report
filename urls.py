import os
from django.conf.urls.defaults import *
from django.conf import settings
from django.views.generic.simple import direct_to_template
from django.contrib import admin
admin.autodiscover()

handler404 = 'weekly_report.apps.util.views.handle_error'
handler500 = 'weekly_report.apps.util.views.handle_error'

urlpatterns = patterns('',
    # pages
    #(r'^admin/', include(admin.site.urls)),

    (r'^$', 'weekly_report.apps.util.views.captured_login'),
    (r'^report/$', 'weekly_report.apps.util.views.created_reports'),
    (r'^generate/$', 'weekly_report.apps.util.views.generate_report'),
    (r'^logout/$', 'weekly_report.apps.accounts.views.logout_user'),

    # processing
    (r'^register_period/$', 'weekly_report.apps.meta.views.store_data'),  
    (r'^process/$', 'weekly_report.apps.accounts.views.ext_login'),    
    
    # fetch data
    (r'^get_compromise_counts/$', 'weekly_report.apps.compromise_data.views.get_compromise_counts'), 
    (r'^get_compromise_details/$', 'weekly_report.apps.compromise_data.views.get_compromise_details'), 
    (r'^get_average_response_time_counts/$', 'weekly_report.apps.compromise_data.views.get_average_response_time_counts'), 
    (r'^get_normal_graph_counts/$', 'weekly_report.apps.compromise_data.views.get_normal_graph_counts'),     
    (r'^get_compromise_types/$', 'weekly_report.apps.compromise_data.views.get_compromise_types'),    
	(r'^get_historical_compromises/$', 'weekly_report.apps.compromise_data.views.get_historical_compromises'), 
	
    (r'^get_stored_compromise_counts/$', 'weekly_report.apps.compromise_data.views.get_stored_compromise_counts'),
    (r'^get_stored_compromise_details/$', 'weekly_report.apps.compromise_data.views.get_stored_compromise_details'),
    (r'^get_stored_average_response_time/$', 'weekly_report.apps.compromise_data.views.get_stored_average_response_time'),
    (r'^get_stored_compromise_types/$', 'weekly_report.apps.compromise_data.views.get_stored_compromise_types'),
    (r'^get_stored_historical_compromises/$', 'weekly_report.apps.compromise_data.views.get_stored_historical_compromises'),
    (r'^get_stored_normal_counts/$', 'weekly_report.apps.compromise_data.views.get_stored_normal_counts'),    
	
	# push data
    (r'^set_compromise_counts/$', 'weekly_report.apps.compromise_data.views.set_compromise_counts'),	
    (r'^set_compromise_details/$', 'weekly_report.apps.compromise_data.views.set_compromise_details'), 
    (r'^set_average_response_times/$', 'weekly_report.apps.compromise_data.views.set_average_response_times'),
    (r'^set_normal_graph_counts/$', 'weekly_report.apps.compromise_data.views.set_normal_graph_counts'),    
    (r'^set_compromise_types/$', 'weekly_report.apps.compromise_data.views.set_compromise_types'),    
    (r'^set_historical_compromises/$', 'weekly_report.apps.compromise_data.views.set_historical_compromises'),  
    
    # reports
    url(r'^report/(?P<rid>\w+)/$', 'weekly_report.apps.builder.views.fetch_report', {'template_name': 'report.html'}, name='report'),   
    
    # aggregate all sources
    (r'^build_report/$', 'weekly_report.apps.builder.views.build_report'),      
    
    # serve static files
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': os.path.join(settings.BASE_DIR, 'media'),
         'show_indexes': False}),
)

