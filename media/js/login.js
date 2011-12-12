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
     'Ext.decode.*',
     'Ext.Msg.*',
     'Ext.EventObject.*',
     'Ext.Ajax.*'
]);

Ext.onReady(function(){

	Ext.QuickTips.init();

    var login = Ext.create('Ext.form.Panel', {
        renderTo:'main_content',
        frame:true,
        title: 'Please Login',
        bodyStyle:'padding:5px 5px 0',
        width: 350,
        fieldDefaults: {
            msgTarget: 'side',
            labelWidth: 75
        },
        defaultType: 'textfield',
        defaults: {
            anchor: '100%',
            listeners: {
                specialkey: function(field, e){
                    if (e.getKey() == e.ENTER) {
                    	var form = this.up('form').getForm();
                        form.submit({
                            clientValidation: true,
                            url: '/process/',
                            success: function(form, action) {
                            	window.location = "/report/";
                            },
                            failure: function(form, action) {
                            	if(action.failureType == 'server') { 
        	                    	obj = Ext.decode(action.response.responseText); 
        	                        Ext.Msg.alert('Login Failed!', obj.error); 
                            	} else {
                                	Ext.Msg.alert('Warning!', 'Authentication server is unreachable');	
                                }
                            	login.getForm().reset(); 
                            }
                        });
                    }
                }
            },
        },

        items: [{
            fieldLabel: 'NetID',
            name: 'netid',
            allowBlank:false
        },{
            fieldLabel: 'Password',
            name: 'password',
            allowBlank:false,
            inputType: 'password',
        }],

        buttons: [{
            text: 'Login',
            formBind: true,
            handler: function() {
                var form = this.up('form').getForm();
                form.submit({
                    clientValidation: true,
                    url: '/process/',
                    success: function(form, action) {
                    	window.location = "/report/";
                    },
                    failure: function(form, action) {
                    	if(action.failureType == 'server') { 
	                    	obj = Ext.decode(action.response.responseText); 
	                        Ext.Msg.alert('Login Failed!', obj.error); 
                    	} else {
                        	Ext.Msg.alert('Warning!', 'Authentication server is unreachable');	
                        }
                    	login.getForm().reset(); 
                    }
                });
            }
        }],

    });
});
