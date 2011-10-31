Ext.Loader.setConfig({
    enabled: true
});
Ext.Loader.setPath('Ext.ux', '/media/extjs/examples/ux');

Ext.require([
     'Ext.grid.*',
     'Ext.data.*',
     'Ext.util.*',
     'Ext.state.*',
     'Ext.form.*',
     'Ext.ux.CheckColumn',
     'Ext.chart.*',
     'Ext.layout.container.Fit',
     'Ext.fx.target.Sprite',
     'Ext.Window',
     'Ext.Action',
     'Ext.button.Button',
]);

var url_parts = window.location.pathname.split('/');
var key = url_parts[2];

Ext.onReady(function(){
	
	Ext.define('WeeklyReport.Compromise.Counts.Model', {
        extend: 'Ext.data.Model',
        fields: [
                 'total_count',
                 'student_count',
                 'staff_faculty_count',
                 'patchlink_count',
                 'non_patchlink_count',
                 'email_count',
                 'key'
         ]
    });

    compromise_counts_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Compromise.Counts.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
            	  read: '/get_stored_compromise_counts/?key=' + key,
            },
            reader: {
                type: 'json',
                root: 'compromise_counts',
                successProperty: 'success'
            },
            writer: {
                type: 'json'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });

    var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
        clicksToMoveEditor: 1,
        autoCancel: false
    });

    // create the grid and specify what field you want
    // to use for the editor at each column.
    var grid = Ext.create('Ext.grid.Panel', {
        store: compromise_counts_store,
        title: "Compromise Counts",
        columns: [{
            header: 'Total',
            dataIndex: 'total_count',
            flex: 1,
            editor: {
                // defaults to textfield if no xtype is supplied
                allowBlank: false
            }
        }, {
            header: 'Student',
            dataIndex: 'student_count',
            width: 160,
            editor: {
                allowBlank: false,
            }
        }, {
            header: 'Faculty/Staff',
            dataIndex: 'staff_faculty_count',
            width: 160,
            editor: {
                allowBlank: false,
            }
        }, {
            header: 'Email',
            dataIndex: 'email_count',
            width: 160,
            editor: {
                allowBlank: false,
            }
        }, {
            header: 'Key',
            dataIndex: 'key',
            flex: 1,
            hidden: true
        }],
        renderTo: 'compromise_counts',
        height: 100,
        frame: true,
    });
    
    //COMPROMISE DETAILS
    
    Ext.define('WeeklyReport.Compromise.Details.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'device_name',
            'ip_address',
            'school_department',
            'time_of_compromise',
            'patchlink_present',
            'last_patchlink_checkin',
            'compromise_notes',
            'original_notes',
            'key'
        ]
    });
    
    compromise_details_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Compromise.Details.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
          	  	read: '/get_stored_compromise_details/?key=' + key,
            },
            reader: {
                type: 'json',
                root: 'compromise_details',
                successProperty: 'success'
            },
            writer: {
                type: 'json'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });

    var rowEditing = Ext.create('Ext.grid.plugin.RowEditing', {
        clicksToMoveEditor: 1,
        autoCancel: false
    });

    // create the grid and specify what field you want
    // to use for the editor at each column.
    var grid = Ext.create('Ext.grid.Panel', {
        store: compromise_details_store,
        title: "Compromise Details",
        columns: [{
            header: 'IP Address',
            dataIndex: 'ip_address',
            flex: 1,
            editor: {
                allowBlank: false
            }
        }, {
            header: 'School/Department',
            dataIndex: 'school_department',
            flex: 1,
            editor: {
                allowBlank: false
            }
        }, {
            header: 'Time of Compromise',
            dataIndex: 'time_of_compromise',
            flex: 1,
            editor: {
                allowBlank: false
            }
        }, {
            header: 'Notes',
            dataIndex: 'compromise_notes',
            flex: 1,
            editor: {
                allowBlank: false
            }
        }, {
            header: 'Key',
            dataIndex: 'key',
            flex: 1,
            hidden: true
        }, {
            header: 'Original Notes',
            dataIndex: 'original_notes',
            flex: 1,
            hidden: true
        }],
        renderTo: 'compromise_details',
        height: 300,
        frame: true,
    });
    
    //Chart Definition
    
    Ext.define('WeeklyReport.Visual.Reporting.Chart.Patchlink.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'name',
            'value',
        ]
    });
    
    var patchy_count_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Visual.Reporting.Chart.Patchlink.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
//                read: 'controls/drafting/get_patchlink_counts.php?start_date='+ start_date + '&end_date='+end_date,
            },
            reader: {
                type: 'json',
                root: 'data',
                successProperty: 'success'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });

//    var panel1 = Ext.create('widget.panel', {
//        width: 350,
//        height: 350,
//        collapsible: true,
//        renderTo: 'pie_chart_one',
//        layout: 'fit',
//        title: "Patchy/Non-Patchy",
//        items: {
//            xtype: 'chart',
//            id: 'pie_chart_one',
//            animate: true,
//            store: patchy_count_store,
//            shadow: true,
//            insetPadding: 60,
//            theme: 'Base:gradients',
//            series: [{
//                type: 'pie',
//                field: 'value',
//                showInLegend: false,
//                tips: {
//                  trackMouse: true,
//                  width: 140,
//                  height: 28,
//                  renderer: function(storeItem, item) {
//                    //calculate percentage.
//                    var total = 0;
//                    patchy_count_store.each(function(rec) {
//                        total += rec.get('value');
//                    });
//                    this.setTitle(storeItem.get('name') + ': ' + Math.round(storeItem.get('value') / total * 100) + '%');
//                  }
//                },
//                highlight: {
//                  segment: {
//                    margin: 20
//                  }
//                },
//                label: {
//                    field: 'name',
//                    display: 'rotate',
//                    contrast: true,
//                    font: '18px Arial'
//                }
//            }]
//        }
//    });
    
    Ext.define('WeeklyReport.Visual.Reporting.Chart.StudentFaculty.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'name',
            'value',
            'key'
        ]
    });
    
    faculty_student_count_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Visual.Reporting.Chart.StudentFaculty.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
            	read: '/get_stored_normal_counts/?key=' + key,
            },
            reader: {
                type: 'json',
                root: 'results',
                successProperty: 'success'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });
    
    var panel2 = Ext.create('widget.panel', {
        width: 450,
        height: 450,
        collapsible: true,
        renderTo: 'pie_chart_two',
        layout: 'fit',
        title: 'Faculty/Student',
        items: {
            xtype: 'chart',
            id: 'pie_chart_two',
            animate: true,
            store: faculty_student_count_store,
            shadow: true,
            insetPadding: 60,
            theme: 'Base:gradients',
            legend: {
                position: 'bottom'
            },
            series: [{
                type: 'pie',
                field: 'value',
                showInLegend: true,
                tips: {
                  trackMouse: true,
                  width: 140,
                  height: 28,
                  renderer: function(storeItem, item) {
                    //calculate percentage.
                    var total = 0;
                    faculty_student_count_store.each(function(rec) {
                        total += rec.get('value');
                    });
                    this.setTitle(storeItem.get('name') + ': ' + Math.round(storeItem.get('value') / total * 100) + '%');
                  }
                },
                highlight: {
                  segment: {
                    margin: 20
                  }
                },
                label: {
                    field: 'name',
                    display: 'rotate',
                    contrast: true,
                    font: '18px Arial',
                	renderer: function(v) {
	            		var gCount = 0;
	                	var total = 0;
	                	faculty_student_count_store.each(function(rec) {
	                    	total += rec.get('value');
	                    });
	
	                	faculty_student_count_store.each(function(rec) {
	                    	if(rec.get('name') == v) {
	                    		gCount = Math.round(rec.get('value') / total * 100) + '%';
	                    	}
	                    });
	               
	            		return gCount;
	            	}
                }
            }]
        }
    });
    
    Ext.define('WeeklyReport.Visual.Reporting.Chart.CompromiseType.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'name',
            'value',
            'key'
        ]
    });
    
    compromise_type_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Visual.Reporting.Chart.CompromiseType.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
        		read: '/get_stored_compromise_types/?key=' + key,
            },
            reader: {
                type: 'json',
                root: 'type_listings',
                successProperty: 'success'
            },
            writer: {
                type: 'json'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });

    var panel3 = Ext.create('widget.panel', {
        width: 450,
        height: 450,
        collapsible: true,
        renderTo: 'pie_chart_three',
        layout: 'fit',
        title: 'Compromise Type',
        items: {
            xtype: 'chart',
            id: 'pie_chart_three',
            animate: true,
            store: compromise_type_store,
            shadow: true,
            insetPadding: 60,
            theme: 'Base:gradients',
            legend: {
                position: 'bottom'
            },
            series: [{
                type: 'pie',
                field: 'value',
                showInLegend: true,
                tips: {
                  trackMouse: true,
                  width: 140,
                  height: 28,
                  renderer: function(storeItem, item) {
                    //calculate percentage.
                    var total = 0;
                    compromise_type_store.each(function(rec) {
                        total += parseInt(rec.get('value')); //storage of the value should NOT be a string
                    });
                    this.setTitle(storeItem.get('name') + ': ' + Math.round(storeItem.get('value') / total * 100) + '%');
                  }
                },
                highlight: {
                  segment: {
                    margin: 20
                  }
                },
                label: {
                    field: 'name',
                    display: 'rotate',
                    contrast: true,
                    font: '18px Arial',
                	renderer: function(v) {
                		var gCount = 0;
                    	var total = 0;
                    	compromise_type_store.each(function(rec) {
                        	total += parseInt(rec.get('value'));
                        });

                    	compromise_type_store.each(function(rec) {
                        	if(rec.get('name') == v) {
                        		gCount = Math.round(parseInt(rec.get('value')) / total * 100) + '%';
                        	}
                        });
                   
                		return gCount;
                	}
                }
            }]
        }
    });
    
    Ext.define('WeeklyReport.Visual.Reporting.Chart.Historic.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'date',
            'current_year',
            'previous_year',
            'current_count',
            'previous_count',
            'key'
        ]
    });
    
    historical_data_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Visual.Reporting.Chart.Historic.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
                read: '/get_stored_historical_compromises/?key=' + key,
            },
            reader: {
                type: 'json',
                root: 'historical_listings',
                successProperty: 'success'
            }
        },
    	sorters: [{
			property: 'start',
			direction: 'ASC'
    	}]
    });
    
    var lDate=new Date();
    var current_year = lDate.getFullYear();
    var previous_year = current_year -1;
    var win = Ext.create('Ext.Panel', {
        width: 1050,
        height: 600,
        hidden: false,
        collapsible: true,
        renderTo: 'line_chart',
        layout: 'fit',
        title: 'Historical Compromise Counts',
        items: {
            xtype: 'chart',
            style: 'background:#fff',
            animate: true,
            store: historical_data_store,
            shadow: true,
            theme: 'Category1',
            legend: {
                position: 'right'
            },
            axes: [{
                type: 'Numeric',
                minimum: 0,
                position: 'left',
                fields: ['current_count','previous_count'],
                title: 'Number of Cases',
                minorTickSteps: 1,
                grid: {
                    odd: {
                        opacity: 1,
                        fill: '#ddd',
                        stroke: '#bbb',
                        'stroke-width': 0.5
                    }
                }
            }, {
                type: 'Category',
                position: 'bottom',
                fields: ['date'],
                title: 'Time Period'
            }],
            series: [{
                type: 'line',
                highlight: {
                    size: 7,
                    radius: 7
                },
                title: current_year,
                smooth: true,
                fill: true,
                axis: 'left',
                xField: 'date',
                yField: 'current_count',
                markerConfig: {
                    type: 'circle',
                    size: 4,
                    radius: 4,
                    'stroke-width': 0
                },
                tips: {
                    trackMouse: true,
                    width: 140,
                    height: 28,
                    renderer: function(storeItem, item) {
                      this.setTitle('Cases: ' + storeItem.get("current_count"));
                    }
                  },
            }, {
                type: 'line',
                highlight: {
                    size: 7,
                    radius: 7
                },
                title: previous_year,
                axis: 'left',
                smooth: true,
                fill: true,
                xField: 'date',
                yField: 'previous_count',
                markerConfig: {
                    type: 'circle',
                    size: 4,
                    radius: 4,
                    'stroke-width': 0
                },
                tips: {
                    trackMouse: true,
                    width: 140,
                    height: 28,
                    renderer: function(storeItem, item) {
                      this.setTitle('Cases: ' + storeItem.get("previous_count"));
                    }
                  },
            }]
        }
    });
});
