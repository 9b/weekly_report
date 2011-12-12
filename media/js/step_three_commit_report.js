function render_commit(id) {
	var action = Ext.create('Ext.Action', {
	    text: 'Commit Report',
	    handler: function(){
			compromise_counts_store.sync();
			compromise_details_store.sync();
			faculty_student_count_store.sync();
			compromise_type_store.sync();
			historical_data_store.sync();
			avg_response_time_store.sync();
			
			Ext.Ajax.request({
			    url: '/build_report/',
			    params: {
			        id: id
			    },
			    success: function(response){
			        var text = response.responseText;
			        // process server response here
					window.location = "/report/" + id;
			    }
			});
			
//			window.location = "/report/" + id;
	    },
	    renderTo:'commit_action'
	});

	Ext.create('Ext.button.Button', action)       // Add the action as a button
}
