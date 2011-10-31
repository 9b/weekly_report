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

Ext.onReady(function(){
	
    Ext.apply(Ext.form.field.VTypes, {
        daterange: function(val, field) {
            var date = field.parseDate(val);

            if (!date) {
                return false;
            }
            if (field.startDateField && (!this.dateRangeMax || (date.getTime() != this.dateRangeMax.getTime()))) {
                var start = field.up('form').down('#' + field.startDateField);
                start.setMaxValue(date);
                start.validate();
                this.dateRangeMax = date;
            }
            else if (field.endDateField && (!this.dateRangeMin || (date.getTime() != this.dateRangeMin.getTime()))) {
                var end = field.up('form').down('#' + field.endDateField);
                end.setMinValue(date);
                end.validate();
                this.dateRangeMin = date;
            }
            /*
             * Always return true since we're only using this vtype to set the
             * min/max allowed values (these are tested for after the vtype test)
             */
            return true;
        },

        daterangeText: 'Start date must be less than end date',
    });
	
    var form = Ext.create('Ext.form.Panel', {
        bodyPadding: '5px 5px 0',
        fieldDefaults: {
            msgTarget: 'side',
            autoFitErrors: false
        },
        defaultType: 'datefield',
        border: false,

        items: [
            {
                fieldLabel: 'Start Date',
                name: 'startdt',
                id: 'startdt',
                vtype: 'daterange',
                endDateField: 'enddt',
            	allowBlank: false
            },
            {
                fieldLabel: 'End Date',
                name: 'enddt',
                id: 'enddt',
                vtype: 'daterange',
                startDateField: 'startdt',
                allowBlank: false
            }
        ],

        buttons: [{
            text: 'Continue',
            handler: function() {
                if (this.up('form').getForm().isValid()) {
                	form.submit({
                        clientValidation: true,
                        url: '/register_period/',
                        success: function(form, action) {
                			win.close();
                			document.getElementById('error').innerHTML = "";
	            			generate_draft(action.result.start_date,action.result.end_date);
	            			document.getElementById('floating_menu').style.visibility='visible';
	            			render_commit(action.result.id);	
                        },
                        failure: function(form,action) {
                        	form.reset();
                        	document.getElementById('error').innerHTML = "<h1 class='title'>Report already present for this time period. Please edit the existing report.</h1>";
                        }
                    });
                }
            }
        }]
    });

    var win = Ext.create('Ext.window.Window', {
        title: 'Pick Time Range',
        width: 300,
        closable: false,
        resizable: false,
        plain: true,
        border: false,
        draggable: false,
        hidden:false,
        layout: 'fit',
        plain:true,
        items: form,
    });

    win.show();
	 
});
