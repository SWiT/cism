YUI().use('node', 'selector-css3', 'event', 'calendar', 'datatype-date', 'io-base', 'io-form', 'node-event-simulate', function (Y) {
	/*
	 * Start Date calendar widget
	 */
	var calStart = new Y.Calendar({
		contentBox: "#cal1Container"
		,showPrevMonth: true
		,showNextMonth: true
		,date: new Date()
	}).render();
	calStart.on("selectionChange", function (ev) {
		var newDate = ev.newSelection[0];
		var dtdate = Y.DataType.Date
		Y.one('#startDateTime').set('value',dtdate.format(newDate)+' 00:00:00');
		Y.one('#cal1Container').hide();
	});
	Y.one('#startDateTime').on('click', function(){
		Y.one('#cal2Container').hide();
		var calCon = Y.one("#cal1Container");
		var tmpstr = (calCon.getStyle('display')=="block")?"none":"block";
		calCon.setStyle('display',tmpstr);
		var xy = Y.one('#startDateTime').getXY()
		xy[0] += 125;
		calCon.setXY(xy);
	});
	
	
	/*
	 * End Date calendar widget
	 */
	var calEnd = new Y.Calendar({
		contentBox: "#cal2Container"
		,showPrevMonth: true
		,showNextMonth: true
		,date: new Date()
	}).render();
	calEnd.on("selectionChange", function (ev) {
		var newDate = ev.newSelection[0];
		var dtdate = Y.DataType.Date
		Y.one("#endDateTime").set('value',dtdate.format(newDate)+' 23:59:59');
		Y.one('#cal2Container').hide();
	});
 	Y.one('#endDateTime').on('click', function(){
		Y.one('#cal1Container').hide();
		var calCon = Y.one("#cal2Container");
		var tmpstr = (calCon.getStyle('display')=="block")?"none":"block";
		calCon.setStyle('display',tmpstr);		
		var xy = Y.one('#endDateTime').getXY()
		xy[0] += 125;
		calCon.setXY(xy);
	});
	
	
	/*
	 * Dropdown to populate start and end dates with a date range based on hours prior to now
	 */
	Y.one('#graphsrange').on('change', function(){
		var hours = Y.one('#graphsrange').get('value');
		if(hours!='---') {
			var objEnd = new Date();
			var objStart = new Date(objEnd - (hours*60*60*1000));
			var dtdate = Y.DataType.Date
			Y.one('#startDateTime').set('value', dtdate.format(objStart, {format:"%Y-%m-%d %H:%M:%S"}));
			Y.one('#endDateTime').set('value', dtdate.format(objEnd, {format:"%Y-%m-%d %H:%M:%S"}));
		}
	});
	var lastrun = new Date();
	Y.later(1000, this, function(){
		if(Y.one('#graphsautoupdate_true').get('checked')){
			var hours = Y.one('#graphsrange').get('value');
			var interval = Y.one('#graphsgetinterval').get('value');
				
			if(hours!='---' && interval > 0) {
				var objEnd = new Date();
				var objStart = new Date(objEnd - (hours*60*60*1000));
				var dtdate = Y.DataType.Date
				Y.one('#startDateTime').set('value', dtdate.format(objStart, {format:"%Y-%m-%d %H:%M:%S"}));
				Y.one('#endDateTime').set('value', dtdate.format(objEnd, {format:"%Y-%m-%d %H:%M:%S"}));
			
				if((lastrun.getTime()+parseInt(interval)) < objEnd.getTime()){
					lastrun = objEnd;
					Y.one('#btngetgraphs').simulate('click');
				}
			}
		}
	},[],true);
	
	/*
	 * Expand/Collapse the various menu and display blocks
	 */
	Y.all("h2.blocktoggle").on('click', function(e){
		var container = e.currentTarget.get('parentNode');
		container.all('div.block').each(function(node){
			var tmpstr = (node.getStyle('display')=="block")?"none":"block";
			node.setStyle('display',tmpstr);
		});
		
		container.all('div.expand-collapse').each(function(node){
			if(node.hasClass('arrow-down')) {
				node.removeClass('arrow-down');
				node.addClass('arrow-right');
			}else{
				node.removeClass('arrow-right');
				node.addClass('arrow-down');
			}
		});
	});
	
	
	/*
	 * Get the graphs 
	 */
	var getgraphs = function(e){
		e.preventDefault();
		e.currentTarget.set('disabled',true);
		Y.all('#graphs .content').setStyle('opacity','0.2');
		var form = {
			id: Y.one('#graphs form').get('id')
			,useDisabled: false
			,upload: false
			};
		var arguments = {'respfor':'getgraphs'};
		var request = Y.io("?rwp=0",{method:"POST", form:form, arguments:arguments});
	};
	Y.one('#btngetgraphs').on('click', getgraphs);
	
	
	
	/*
	 * Refresh Statuses
	 */
	Y.one('#btnrefreshstatuses').on('click', function(e){
		e.preventDefault();
		e.currentTarget.set('disabled',true);
		Y.all('#statuses .content').setStyle('opacity','0.2');
		var form = {
			id: Y.one('#statuses form').get('id')
			,useDisabled: false
			,upload: false
			};
		var arguments = {'respfor':'refreshstatuses'};
		var request = Y.io("?rwp=0",{method:"POST", form:form, arguments:arguments});
	});
	
	
	/*
	 * IODevice Events
	 */
	bindevents_iodevices = function(){
		// Add
		Y.one('#iodevice_add').on('click', function(e){rpccall(e, {'command':'iodevices'});});
		
		// Cancel
		Y.all('#iodevices button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'iodevices'});});
		
		// Save
		Y.all('#iodevices button[value="save"]').on('click', function(e){
			var indexedfields = ['iodevice_id','iodevice_label','iodevice_port','iodevice_timeout','iodevice_baud','iodevice_samplerate'];
			rpccall(e, {'command':'iodevices'}, indexedfields);
		});
		
		// Edit
		Y.all('#iodevices button[value="edit"]').on('click', function(e){rpccall(e, {'command':'iodevices'}, ['iodevice_id']);});
		
		// Remove
		Y.all('#iodevices button[value="remove"]').on('click', function(e){rpccall(e, {'command':'iodevices'}, ['iodevice_id']);});
		
		// Remove Confirm Yes
		//Y.one('#iodevice_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#iodevice_confirm_no').on('click', function(e){rpccall(e, {'command':'iodevices'});});
	};
	bindevents_iodevices();
	unbindevents_iodevices = function(){
		Y.all('#iodevices button').detach('click');
	};
	
	
	/*
	 * Input Events
	 */
	bindevents_inputs = function(){
		// Add
		Y.one('#input_add').on('click', function(e){rpccall(e, {'command':'inputs'});});
		
		// Cancel
		Y.all('#inputs button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'inputs'});});
		
		// Save
		Y.all('#inputs button[value="save"]').on('click', function(e){
			var indexedfields = ['input_id','input_iodevice','input_pin','input_type','input_label','input_color'];
			rpccall(e, {'command':'inputs'}, indexedfields);
		});
		
		// Edit
		Y.all('#inputs button[value="edit"]').on('click', function(e){rpccall(e, {'command':'inputs'}, ['input_id']);});
		
		// Remove
		Y.all('#inputs button[value="remove"]').on('click', function(e){rpccall(e, {'command':'inputs'}, ['input_id']);});
		
		// Remove Confirm Yes
		//Y.one('#output_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#input_confirm_no').on('click', function(e){rpccall(e, {'command':'inputs'});});
	};
	bindevents_inputs();
	unbindevents_inputs = function(){
		Y.all('#inputs button').detach('click');
	};
	
	
	/*
	 * Output Events
	 */
	bindevents_outputs = function(){
		// Add
		Y.one('#output_add').on('click', function(e){rpccall(e, {'command':'outputs'});});
		
		// Cancel
		Y.all('#outputs button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'outputs'});});
		
		// Save
		Y.all('#outputs button[value="save"]').on('click', function(e){
			var indexedfields = ['output_id','output_iodevice','output_pin','output_type','output_label','output_color'];
			rpccall(e, {'command':'outputs'}, indexedfields);
		});
		
		// Edit
		Y.all('#outputs button[value="edit"]').on('click', function(e){rpccall(e, {'command':'outputs'}, ['output_id']);});
		
		// Remove
		Y.all('#outputs button[value="remove"]').on('click', function(e){rpccall(e, {'command':'outputs'}, ['output_id']);});
		
		// Remove Confirm Yes
		//Y.one('#output_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#output_confirm_no').on('click', function(e){rpccall(e, {'command':'outputs'});});
	};
	bindevents_outputs();
	unbindevents_outputs = function(){
		Y.all('#outputs button').detach('click');
	};
	
	/*
	 * Output Types Events
	 */
	bindevents_outputtypes = function(){
		// Add
		Y.one('#outputtype_add').on('click', function(e){rpccall(e, {'command':'outputtypes'});});
		
		// Cancel
		Y.all('#outputtypes button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'outputtypes'});});
		
		// Save
		Y.all('#outputtypes button[value="save"]').on('click', function(e){
			var indexedfields = ['outputtype_id','outputtype_name','outputtype_rangebegin','outputtype_rangeend','outputtype_maxupdaterate'];
			var indexedsubfields = ['outputtype_ovlid','outputtype_label','outputtype_value'];
			rpccall(e, {'command':'outputtypes'}, indexedfields, indexedsubfields);
		});
		
		// Edit
		Y.all('#outputtypes button[value="edit"]').on('click', function(e){rpccall(e, {'command':'outputtypes'}, ['outputtype_id']);});
		
		// Remove
		Y.all('#outputtypes button[value="remove"]').on('click', function(e){rpccall(e, {'command':'outputtypes'}, ['outputtype_id']);});
		
		// Remove Confirm Yes
		//Y.one('#outputtype_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#outputtype_confirm_no').on('click', function(e){rpccall(e, {'command':'outputtypes'});});
		
		// Add Label
		Y.all('#outputtypes button[value="addvaluelabel"]').on('click', function(e){rpccall(e, {'command':'outputtypes'}, ['outputtype_id']);});
	};
	bindevents_outputtypes();
	unbindevents_outputtypes = function(){
		Y.all('#outputtypes button').detach('click');
	};
	
	/*
	 * Input Types Events
	 */
	bindevents_inputtypes = function(){
		// Add
		Y.one('#inputtype_add').on('click', function(e){rpccall(e, {'command':'inputtypes'});});
		
		// Cancel
		Y.all('#inputtypes button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'inputtypes'});});
		
		// Save
		Y.all('#inputtypes button[value="save"]').on('click', function(e){
			var indexedfields = ['inputtype_id','inputtype_name','inputtype_maxsamplerate'];
			var indexedsubfields = ['inputtype_idtid','inputtype_label','inputtype_unit','inputtype_rangebegin','inputtype_rangeend','inputtype_accuracy'];
			rpccall(e, {'command':'inputtypes'}, indexedfields, indexedsubfields);
		});
		
		// Edit
		Y.all('#inputtypes button[value="edit"]').on('click', function(e){rpccall(e, {'command':'inputtypes'}, ['inputtype_id']);});
		
		// Remove
		Y.all('#inputtypes button[value="remove"]').on('click', function(e){rpccall(e, {'command':'inputtypes'}, ['inputtype_id']);});
		
		// Remove Confirm Yes
		//Y.one('#inputtype_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#inputtype_confirm_no').on('click', function(e){rpccall(e, {'command':'inputtypes'});});
		
		// Add Data Type
		Y.all('#inputtypes button[value="adddatatype"]').on('click', function(e){rpccall(e, {'command':'inputtypes'}, ['inputtype_id']);});
	};
	bindevents_inputtypes();
	unbindevents_inputtypes = function(){
		Y.all('#inputtypes button]').detach('click');
	};
	
	
	/*
	 * Graph Settings Events
	 */
	bindevents_graphsettings = function(){
		// Add
		Y.one('#graph_add').on('click', function(e){rpccall(e, {'command':'graphsettings'});});
		
		// Cancel
		Y.all('#graphsettings button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'graphsettings'});});
		
		// Save
		Y.all('#graphsettings button[value="save"]').on('click', function(e){
			var indexedfields = ['graph_id','graph_label','graph_inputdatatypeid','graph_io'];
			rpccall(e, {'command':'graphsettings'}, indexedfields);
		});
		
		// Edit
		Y.all('#graphsettings button[value="edit"]').on('click', function(e){rpccall(e, {'command':'graphsettings'}, ['graph_id']);});
		
		// Remove
		Y.all('#graphsettings button[value="remove"]').on('click', function(e){rpccall(e, {'command':'graphsettings'}, ['graph_id']);});

		// Remove Confirm Yes
		//Y.one('#graph_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#graph_confirm_no').on('click', function(e){rpccall(e, {'command':'graphsettings'});});
		
		// Remove Entry
		Y.all('#graphsettings #remove_entry').on('click', function(e){
			var itemid = Y.one('#itemid').get('value')
			rpccall(e, {'command':'graphsettings','itemid':itemid});
		});
		
		// Add Entry
		Y.all('#graphsettings #add_entry').on('click', function(e){
			data = {'command':'graphsettings'
					, 'graph_entry': Y.one('#graph_entry').get('value')
					};
			rpccall(e, data);
		});
	};
	bindevents_graphsettings();
	unbindevents_graphsettings = function(){
		Y.all('#inputtypes button').detach('click');
	};
	
	
	
	/*
	 * Rules Events
	 */
	bindevents_rules = function(){
		// Add
		Y.one('#rule_add').on('click', function(e){rpccall(e, {'command':'rules'});});
		
		// Cancel
		Y.all('#rules button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'rules'});});
		
		// Save
		Y.all('#rules button[value="save"]').on('click', function(e){
			var indexedfields = ['rule_id'
								, 'rule_sourcetype'
								, 'rule_sourceoutputid'
								, 'rule_sourceinputid'
								, 'rule_operation'
								, 'rule_comparetype'
								, 'rule_comparevalue'
								, 'rule_compareoutputid'
								, 'rule_compareinputid'
								, 'rule_outcomeid'
								, 'rule_outcomevalue'
								, 'rule_priority'
								];
			rpccall(e, {'command':'rules'}, indexedfields);
		});
		
		// Edit
		Y.all('#rules button[value="edit"]').on('click', function(e){rpccall(e, {'command':'rules'}, ['rule_id']);});
		
		// Remove
		Y.all('#rules button[value="remove"]').on('click', function(e){rpccall(e, {'command':'rules'}, ['rule_id']);});
		
		// Remove Confirm Yes
		//Y.one('#rule_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#rule_confirm_no').on('click', function(e){rpccall(e, {'command':'rules'});});
	};
	bindevents_rules();
	unbindevents_rules = function(){
		Y.all('#rules button').detach('click');
	};
	
	
	/*
	 * Users Events
	 */
	bindevents_users = function(){
		// Add
		Y.one('#user_add').on('click', function(e){rpccall(e, {'command':'users'});});
		
		// Cancel
		Y.all('#users button[value="cancel"]').on('click', function(e){rpccall(e, {'command':'users'});});
		
		// Save
		Y.all('#users button[value="save"]').on('click', function(e){
			var indexedfields = ['user_id'
								, 'user_username'
								, 'user_password'
								];
			rpccall(e, {'command':'users'}, indexedfields);
		});
		
		// Edit
		Y.all('#users button[value="edit"]').on('click', function(e){rpccall(e, {'command':'users'}, ['user_id']);});
		
		// Remove
		Y.all('#users button[value="remove"]').on('click', function(e){rpccall(e, {'command':'users'}, ['user_id']);});
		
		// Remove Confirm Yes
		//Y.one('#user_confirm_yes').on('click', function(e){});
		
		// Remove Confirm No
		Y.all('#user_confirm_no').on('click', function(e){rpccall(e, {'command':'users'});});
	};
	bindevents_users();
	unbindevents_users = function(){
		Y.all('#users button').detach('click');
	};
	
	
	
	/*
	 * Handle IO responses
	 */
	Y.on('io:success', function(id, o, args) {
		if(args.respfor=='getgraphs') {
			Y.one('#graphs div.content').setHTML(o.responseText);
			Y.one('#btngetgraphs').set('disabled',false);
			Y.all('#graphs .content').setStyle('opacity','');
			
		} else if (args.respfor=='refreshstatuses') {
			Y.all('#statuses .content').setStyle('opacity','');
			Y.one('#statuses div.content').setHTML(o.responseText);
			Y.one('#btnrefreshstatuses').set('disabled',false);
		
		} else if (args.respfor!='') {
			Y.one('#'+args.respfor+' form').setStyle('opacity','');
			window['unbindevents_'+args.respfor]();
			Y.one('#'+args.respfor+' form').setHTML(o.responseText);
			window['bindevents_'+args.respfor]();
			Y.all('#'+args.respfor+' button').set('disabled',false);
		}
	});
	
	Y.on('io:failure', function(id, o, args) {
		if(args.respfor=='getgraphs') {
			Y.one('#btngetgraphs').set('disabled',false);
			Y.all('#graphs .content').setStyle('opacity','');
			
		} else if (args.respfor=='refreshstatuses') {
			Y.all('#statuses .content').setStyle('opacity','');
			Y.one('#btnrefreshstatuses').set('disabled',false);
			
		} else if (args.respfor!='') {
			Y.all('#'+args.respfor+' form').setStyle('opacity','');
			Y.one('#'+args.respfor+' button').set('disabled',false);
		}
	});
	
	
	/*
	 * Utilities
	 */
	var rpccall = function(e, data, indexedfields, indexedsubfields){
			e.preventDefault();
			var savebtnid = e.currentTarget.get('id');
			data[savebtnid] = e.currentTarget.get('value'); //add the id and value of the clicked button
			var idx = savebtnid.split("_");
			if(idx.length==3){
				idx = idx[2];
				if(indexedfields!=undefined){
					var id;
					for(var i=0; i<indexedfields.length; i++){
						id = indexedfields[i]+'_'+idx;
						data[id] = Y.one('#'+id).get('value');
					}
					
					if(indexedsubfields!=undefined){
						var grouping, sidx;
						for(var i=0; i<indexedsubfields.length; i++){
							grouping = indexedsubfields[i]+'_'+idx+'_';
							sidx = 0;
							while(Y.one('#'+grouping+sidx)){
								id = grouping+sidx;
								data[id] = Y.one('#'+id).get('value');
								sidx++;
							}
						}
					}
				}
			}
			
			var arguments = {'respfor':data.command};
			var request = Y.io("?rwp=0",{method:"POST", data:data, arguments:arguments});
			
			e.currentTarget.set('disabled',true);
			Y.one('#'+data.command+' form').setStyle('opacity','0.2');
		};
	
});
