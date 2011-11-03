var compromise_counts_store;
var compromise_details_store;
var faculty_student_count_store;
var compromise_type_store;
var historical_data_store;
var avg_response_time_store;

function generate_draft(start_date,end_date) {
    // Define our data model
    Ext.define('WeeklyReport.Compromise.Counts.Model', {
        extend: 'Ext.data.Model',
        fields: [
                 'total_count',
                 'student_count',
                 'staff_faculty_count',
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
            	  read: '/get_compromise_counts/?start_date=' + start_date + '&end_date=' + end_date,
            	  create: '/set_compromise_counts/',
        		  update: '/set_compromise_counts/'
            },
            reader: {
                type: 'json',
                root: 'results',
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
        height: 250,
        frame: true,
        plugins: [rowEditing],
    });
    
    //COMPROMISE DETAILS
    
    Ext.define('WeeklyReport.Compromise.Details.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'ip_address',
            'school_department',
            'time_of_compromise',
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
            	  read: '/get_compromise_details/?start_date=' + start_date + '&end_date=' + end_date,
            	  create: '/set_compromise_details/',
            	  update: '/set_compromise_details/'
            },
            reader: {
                type: 'json',
                root: 'results',
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
        tbar: [{
            text: 'Add Compromise',
            iconCls: 'add-compromise',
            handler : function() {
                rowEditing.cancelEdit();

                // Create a record instance through the ModelManager
                var r = Ext.ModelManager.create({
                	device_name: '',
                	ip_address: '',
                	school_department: '',
                	time_of_compromise: '',
                	patchlink_present: '',
                	last_patchlink_checkin: '',
                	compromise_notes: ' '
                }, 'WeeklyReport.Compromise.Details.Model');

                compromise_details_store.insert(0, r);
                rowEditing.startEdit(0, 0);
            }
        }, {
            itemId: 'remove_compromise',
            text: 'Remove Compromise',
            iconCls: 'remove-compromise',
            handler: function() {
                var sm = grid.getSelectionModel();
                rowEditing.cancelEdit();
                compromise_details_store.remove(sm.getSelection());
                if (compromise_details_store.getCount() > 0) {
                    sm.select(0);
                }
            },
            disabled: true
        }],
        plugins: [rowEditing],
        listeners: {
            'selectionchange': function(view, records) {
                grid.down('#remove_compromise').setDisabled(!records.length);
            }
        }
    });
    
    //Chart Definition
    
    Ext.define('WeeklyReport.Visual.Reporting.Chart.ResponseTime.Model', {
        extend: 'Ext.data.Model',
        fields: [
            'name',
            'value',
            'key'
        ]
    });
    
    avg_response_time_store = Ext.create('Ext.data.Store', {
        model: 'WeeklyReport.Visual.Reporting.Chart.ResponseTime.Model',
        autoLoad: true,

        proxy: {
            type: 'ajax',
            api: {
            	read: '/get_average_response_time_counts/?start_date='+ start_date + '&end_date='+end_date,
            	create: '/set_average_response_times/',
            	update: '/set_average_response_times/'
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
    
    var imageTpl = new Ext.XTemplate(
		'<tpl for=".">',
        	'<h1 class="response_content">{value} Hours</h1>',
	    '</tpl>'
	);
    
    var average_response_time = new Ext.create('Ext.view.View', {
        store: avg_response_time_store,
        tpl: imageTpl,
        itemSelector: 'div.thumb-wrap',
        emptyText: 'No images available',
    });

    var panel1 = Ext.create('widget.panel', {
        width: 350,
        height: 450,
        collapsible: true,
        renderTo: 'pie_chart_one',
        layout: 'fit',
        title: 'Average Response Time',
        items: [average_response_time]
    });
    
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
            	read: '/get_normal_graph_counts/?start_date='+ start_date + '&end_date='+end_date,
            	create: '/set_normal_graph_counts/',
            	update: '/set_normal_graph_counts/'
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
        width: 350,
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
        		read: '/get_compromise_types/?start_date='+ start_date + '&end_date='+end_date,
                create: '/set_compromise_types/',
                update: '/set_compromise_types/'
            },
            reader: {
                type: 'json',
                root: 'results',
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
        width: 350,
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
                read: '/get_historical_compromises/?start_date='+ start_date + '&end_date='+end_date,
                create: '/set_historical_compromises/',
                update: '/set_historical_compromises/'
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
}
