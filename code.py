import os
import web
import serial
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import hashlib
import ConfigParser

curdir = os.path.dirname(__file__)

config = ConfigParser.ConfigParser()
config.read(os.path.join(curdir,'cism.cfg'))

render = web.template.render(os.path.join(curdir,'templates'), globals={ 'str':str, 'type':type, 'int':int})

urls = ('/.*', 'index')

db = web.database(dbn=config.get('Database','dbn')
				, user=config.get('Database','user')
				, pw=config.get('Database','pw')
				, db=config.get('Database','db')
				)
	
class index:
	def POST(self):	
		f = web.input()
		
		#Log out
		if isset(f,'logout'):
			del session.username
			session.kill()
			return renderWholePage(self)
		
		#Check if logged in
		if not isset(session, 'username'):
			if f.command=="login" and isset(f, 'login_username') and isset(f, 'login_password'):
				pwdhash = hashlib.md5(f.login_username+f.login_password).hexdigest()
				users = db.select('cism_users'
						, where = "username=$username and password=$password"
						, vars={'username':f.login_username, 'password':pwdhash}
						)
				if len(users) == 1:
					session.username = f.login_username
					return renderWholePage(self)
				else:
					return "LOGIN_FAILED"
			return "LOGIN_REQUIRED"
		
		#Get Graphs
		if f.command=="getgraphs":
			dtStart = datetime.strptime(f.startDateTime, "%Y-%m-%d %H:%M:%S")
			dtEnd = datetime.strptime(f.endDateTime, "%Y-%m-%d %H:%M:%S")
			data = {"now":datetime.now()
				, "dtStart":dtStart
				, "dtEnd":dtEnd
				}
			return renderGraphs(self, data)

		#Graph Settings
		elif f.command=="graphsettings":
			graphs = getGraphs()
			i = -1
			for i in range(0,len(graphs)):
				#edit
				if isset(f, "graph_edit_"+str(i)):
					itemid = int(getattr(f,"graph_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderGraphSettingsForm(self, graphs=graphs, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='graphsettings', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "graph_remove_"+str(i)):
					itemid = int(getattr(f,"graph_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderGraphSettingsForm(self, graphs=graphs, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='graphsettings', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "graph_confirm_action") and isset(f, "graph_confirm_yes"):
					if f.graph_confirm_action=='remove' and f.graph_confirm_yes=='yes':
						itemid = int(getattr(f,"graph_confirm_itemid"))
						db.delete('graph', where="id=$id", vars={'id':itemid})
						if isRenderWholePageOff(f):
							return renderGraphSettingsForm(self)
						else:
							return renderWholePage(self, block='graphsettings') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "graph_save_"+str(i)):
					saveGraph(f, i)
					if isRenderWholePageOff(f):
						return renderGraphSettingsForm(self)
					else:
						return renderWholePage(self)
				
			#add graph form
			if isset(f, "graph_add"):
				if isRenderWholePageOff(f):
					return renderGraphSettingsForm(self, graphs=graphs, mode='add')
				else:
					return renderWholePage(self, block='graphsettings', mode='add')
					
			#add graph
			i += 1 
			if isset(f, "graph_save_"+str(i)):
				saveGraph(f, i)
				
			#remove entry
			if isset(f, "remove_entry") and isset(f, "itemid"):
				db.delete('graph_entries', where='id=$id', vars={'id':f.remove_entry})
				if isRenderWholePageOff(f):
					return renderGraphSettingsForm(self, mode='edit', itemid=f.itemid)
				else:
					return renderWholePage(self, block='graphsettings', mode='edit', itemid=f.itemid)	
				
			#add entry
			if isset(f, "graph_entry") and isset(f, "add_entry"):
				itemid = f.add_entry
				db.insert('graph_entries', ioid=f.graph_entry, graphid=itemid)
				if isRenderWholePageOff(f):
					return renderGraphSettingsForm(self, mode='edit', itemid=itemid)
				else:
					return renderWholePage(self, block='graphsettings', mode='edit', itemid=itemid)	
			
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderGraphSettingsForm(self)
			else:
				return renderWholePage(self)
			
		#IODevice
		elif f.command=="iodevices":
			iodevices = getIODevices()
			for i in range(0,len(iodevices)):
				#edit
				if isset(f, "iodevice_edit_"+str(i)):
					itemid = int(getattr(f,"iodevice_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderIODeviceForm(self, iodevices, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='iodevices', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "iodevice_remove_"+str(i)):
					itemid = int(getattr(f,"iodevice_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderIODeviceForm(self, iodevices, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='iodevices', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "iodevice_confirm_action") and isset(f, "iodevice_confirm_yes"):
					if f.iodevice_confirm_action=='remove' and f.iodevice_confirm_yes=='yes':
						itemid = int(getattr(f,"iodevice_confirm_itemid"))
						db.delete('io_device', where="id=$id", vars={'id':itemid})
						iodevices = getIODevices()
						if isRenderWholePageOff(f):
							return renderIODeviceForm(self, iodevices)
						else:
							return renderWholePage(self, block='iodevices') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "iodevice_save_"+str(i)):
					saveIODevice(f, i)
					iodevices = getIODevices()
					if isRenderWholePageOff(f):
						return renderIODeviceForm(self, iodevices)
					else:
						return renderWholePage(self)
					
			#add iodevice form
			if isset(f, "iodevice_add"):
				if isRenderWholePageOff(f):
					return renderIODeviceForm(self, iodevices, mode='add')
				else:
					return renderWholePage(self, block='iodevices', mode='add')
					
			#add iodevice
			i += 1 
			if isset(f, "iodevice_save_"+str(i)):
				saveIODevice(f, i)
				iodevices = getIODevices()
				
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderIODeviceForm(self, iodevices)
			else:
				return renderWholePage(self)
				
		#Input
		elif f.command=="inputs":
			inputs = getInputs()
			for i in range(0,len(inputs)):
				#edit
				if isset(f, "input_edit_"+str(i)):
					itemid = int(getattr(f,"input_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderInputForm(self, inputs, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='inputs', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "input_remove_"+str(i)):
					itemid = int(getattr(f,"input_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderInputForm(self, inputs, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='inputs', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "input_confirm_action") and isset(f, "input_confirm_yes"):
					if f.input_confirm_action=='remove' and f.input_confirm_yes=='yes':
						itemid = int(getattr(f,"input_confirm_itemid"))
						db.delete('input', where="id=$id", vars={'id':itemid})
						inputs = getInputs()
						if isRenderWholePageOff(f):
							return renderInputForm(self, inputs)
						else:
							return renderWholePage(self, block='inputs') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "input_save_"+str(i)):
					saveInput(f, i)
					inputs = getInputs()
					if isRenderWholePageOff(f):
						return renderInputForm(self, inputs)
					else:
						return renderWholePage(self)
				
			#add input form
			if isset(f, "input_add"):
				if isRenderWholePageOff(f):
					return renderInputForm(self, inputs, mode='add')
				else:
					return renderWholePage(self, block='inputs', mode='add')
					
			#add input
			i += 1 
			if isset(f, "input_save_"+str(i)):
				saveInput(f, i)
				inputs = getInputs()
				
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderInputForm(self, inputs)
			else:
				return renderWholePage(self)
			
		#Output
		elif f.command=="outputs":
			outputs = getOutputs()
			for i in range(0,len(outputs)):
				#edit
				if isset(f, "output_edit_"+str(i)):
					itemid = int(getattr(f,"output_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderOutputForm(self, outputs, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='outputs', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "output_remove_"+str(i)):
					itemid = int(getattr(f,"output_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderOutputForm(self, outputs, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='outputs', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "output_confirm_action") and isset(f, "output_confirm_yes"):
					if f.output_confirm_action=='remove' and f.output_confirm_yes=='yes':
						itemid = int(getattr(f,"output_confirm_itemid"))
						db.delete('output', where="id=$id", vars={'id':itemid})
						outputs = getOutputs()
						if isRenderWholePageOff(f):
							return renderOutputForm(self, outputs)
						else:
							return renderWholePage(self, block='outputs') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "output_save_"+str(i)):
					saveOutput(f, i)
					outputs = getOutputs()
					if isRenderWholePageOff(f):
						return renderOutputForm(self, outputs)
					else:
						return renderWholePage(self)
				
				
			#add output form
			if isset(f, "output_add"):
				if isRenderWholePageOff(f):
					return renderOutputForm(self, outputs, mode='add')
				else:
					return renderWholePage(self, block='outputs', mode='add')
					
			#add output
			i += 1 
			if isset(f, "output_save_"+str(i)):
				saveOutput(f, i)		
				outputs = getOutputs()
				
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderOutputForm(self, outputs)
			else:
				return renderWholePage(self)
		
		#Statuses
		elif f.command=="refreshstatuses":
			data = {"now":datetime.now()
					,"statuses":getStatuses()
					}
			return renderStatuses(self, data)
		
		#Input Types
		elif f.command=="inputtypes":
			inputtypes = getInputTypes()
			for i in range(0,len(inputtypes)):
				#edit
				if isset(f, "inputtype_edit_"+str(i)):
					itemid = int(getattr(f,"inputtype_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderInputTypesForm(self, getInputTypeWithDataTypes(), mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='inputtypes', mode='edit', itemid=itemid)	

				#remove - confirm dialog
				if isset(f, "inputtype_remove_"+str(i)):
					itemid = int(getattr(f,"inputtype_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderInputTypesForm(self, getInputTypeWithDataTypes(), mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='inputtypes', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "inputtype_confirm_action") and isset(f, "inputtype_confirm_yes"):
					if f.inputtype_confirm_action=='remove' and f.inputtype_confirm_yes=='yes':
						itemid = int(getattr(f,"inputtype_confirm_itemid"))
						db.delete('input_data_type', where="inputtypeid=$inputtypeid", vars={'inputtypeid':itemid})
						db.delete('input_type', where="id=$id", vars={'id':itemid})
						if isRenderWholePageOff(f):
							return renderOutputTypesForm(self, getInputTypeWithDataTypes())
						else:
							return renderWholePage(self, block='inputtypes') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "inputtype_save_"+str(i)):
					saveInputType(f, i)
					saveInputDataTypes(f, i)
				
			#display add input type form
			if isset(f, "inputtype_add"):
				if isRenderWholePageOff(f):
					return renderInputTypesForm(self, getInputTypeWithDataTypes(), mode='add')
				else:
					return renderWholePage(self, block='inputtypes', mode='add')
				
			#add new output type
			i += 1 
			if isset(f, "inputtype_save_"+str(i)):
				saveInputType(f, i)			
				
			#view mode, no action, or cancel
			if isRenderWholePageOff(f):
				return renderInputTypesForm(self, getInputTypeWithDataTypes())
			else:
				return renderWholePage(self)
		
		#Output Types
		elif f.command=="outputtypes":
			outputtypes = getOutputTypes()
			for i in range(0,len(outputtypes)):
				#edit
				if isset(f, "outputtype_edit_"+str(i)):
					itemid = int(getattr(f,"outputtype_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderOutputTypesForm(self, getOutputTypeWithValueLabels(), mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='outputtypes', mode='edit', itemid=itemid)			
				
				#remove - confirm dialog
				if isset(f, "outputtype_remove_"+str(i)):
					itemid = int(getattr(f,"outputtype_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderOutputTypesForm(self, getOutputTypeWithValueLabels(), mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='outputtypes', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "outputtype_confirm_action") and isset(f, "outputtype_confirm_yes"):
					if f.outputtype_confirm_action=='remove' and f.outputtype_confirm_yes=='yes':
						itemid = int(getattr(f,"outputtype_confirm_itemid"))
						db.delete('output_value_labels', where="outputtypeid=$outputtypeid", vars={'outputtypeid':itemid})
						db.delete('output_type', where="id=$id", vars={'id':itemid})
						if isRenderWholePageOff(f):
							return renderOutputTypesForm(self, getOutputTypeWithValueLabels())
						else:
							return renderWholePage(self, block='outputtypes') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "outputtype_save_"+str(i)):
					saveOutputType(f, i)
					saveOutputValueLabels(f, i)
						
				#add value label fields
				if isset(f, "outputtype_addvaluelabel_"+str(i)):
					itemid = int(getattr(f,"outputtype_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderOutputTypesForm(self, getOutputTypeWithValueLabels(), mode='edit', itemid=itemid, extra = True)
					else:
						return renderWholePage(self, block='outputtypes', mode='edit', itemid=itemid, extra = True)
					
			#display add output type form
			if isset(f, "outputtype_add"):
				if isRenderWholePageOff(f):
					return renderOutputTypesForm(self, getOutputTypeWithValueLabels(), mode='add')
				else:
					return renderWholePage(self, block='outputtypes', mode='add')
				
			#add new output type
			i += 1 
			if isset(f, "outputtype_save_"+str(i)):
				saveOutputType(f, i)			
			
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderOutputTypesForm(self, getOutputTypeWithValueLabels())
			else:
				return renderWholePage(self)
		
		#Rules
		elif f.command=="rules":
			rules = getRules()
			i = -1
			for i in range(0,len(rules)):
				#edit
				if isset(f, "rule_edit_"+str(i)):
					itemid = int(getattr(f,"rule_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderRulesForm(self, rules, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='rules', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "rule_remove_"+str(i)):
					itemid = int(getattr(f,"rule_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderRulesForm(self, rules, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='rules', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "rule_confirm_action") and isset(f, "rule_confirm_yes"):
					if f.rule_confirm_action=='remove' and f.rule_confirm_yes=='yes':
						itemid = int(getattr(f,"rule_confirm_itemid"))
						db.delete('rule', where="id=$id", vars={'id':itemid})
						rules = getRules()
						if isRenderWholePageOff(f):
							return renderRulesForm(self, rules)
						else:
							return renderWholePage(self, block='rules') #TODO: needs remove sucessful message
				
				#save
				if isset(f, "rule_save_"+str(i)):
					saveRule(f, i)
					rules = getRules()
					if isRenderWholePageOff(f):
						return renderRulesForm(self, rules)
					else:
						return renderWholePage(self)
					
			#add rule form
			if isset(f, "rule_add"):
				if isRenderWholePageOff(f):
					return renderRulesForm(self, rules, mode='add')
				else:
					return renderWholePage(self, block='rules', mode='add')
					
			#add rule
			i += 1 
			if isset(f, "rule_save_"+str(i)):
				saveRule(f, i)
				rules = getRules()
				
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderRulesForm(self, rules)
			else:
				return renderWholePage(self)
				
		#Users
		elif f.command=="users":
			users = getUsers()
			i = -1
			for i in range(0,len(users)):
				#edit
				if isset(f, "user_edit_"+str(i)):
					itemid = int(getattr(f,"user_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderUsersForm(self, users, mode='edit', itemid=itemid)
					else:
						return renderWholePage(self, block='users', mode='edit', itemid=itemid)	
				
				#remove - confirm dialog
				if isset(f, "user_remove_"+str(i)):
					itemid = int(getattr(f,"user_id_"+str(i)))
					if isRenderWholePageOff(f):
						return renderUsersForm(self, users, mode='remove', itemid=itemid)
					else:
						return renderWholePage(self, block='users', mode='remove', itemid=itemid)
				
				#remove confirmed
				if isset(f, "user_confirm_action") and isset(f, "user_confirm_yes"):
					if f.user_confirm_action=='remove' and f.user_confirm_yes=='yes':
						itemid = int(getattr(f,"user_confirm_itemid"))
						db.delete('cism_users', where="id=$id", vars={'id':itemid})
						users = getUsers()
						if isRenderWholePageOff(f):
							return renderUsersForm(self, users)
						else:
							return renderWholePage(self, block='users') #TODO: needs remove sucessful mesage
				
				#save
				if isset(f, "user_save_"+str(i)):
					saveUser(f, i)
					users = getUsers()
					if isRenderWholePageOff(f):
						return renderUsersForm(self, users)
					else:
						return renderWholePage(self)
					
			#add user form
			if isset(f, "user_add"):
				if isRenderWholePageOff(f):
					return renderUsersForm(self, users, mode='add')
				else:
					return renderWholePage(self, block='users', mode='add')
					
			#add user
			i += 1 
			if isset(f, "user_save_"+str(i)):
				saveUser(f, i)
				users = getUsers()
				
			#view mode or no action requested
			if isRenderWholePageOff(f):
				return renderUsersForm(self, users)
			else:
				return renderWholePage(self)
		
		else:
			return renderOutcome(self, 'COMMAND_NOT_RECOGNIZED')

	def GET(self):
		#Log out
		f = web.input()
		if isset(f,'logout') and isset(session,'username'):
			del session.username
			session.kill()
		return renderWholePage(self)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore(os.path.join(curdir,'sessions')),)
app.internalerror = web.debugerror
if __name__ == "__main__":
	app.run()
else:
	application = app.wsgifunc()

	
#---------------------------------------------------------------------	
# RENDERERS
#---------------------------------------------------------------------

def renderWholePage(self, block=None, mode='view', itemid=None, extra=None):	
	
	pagedata = {"content":{}, "forms":{}}
	
	if not isset(session, 'username'):
		pagedata["content"]["login"] = ""
		pagedata["forms"]["login"] = renderLoginForm(self)
		return render.login(pagedata)
	
	now = datetime.now()
	dtStart = now + timedelta(hours=-8)
	dtEnd = now
	iodevices = getIODevices()
	inputs = getInputs()
	outputs = getOutputs()
	inputtypes = getInputTypeWithDataTypes();
	outputtypes = getOutputTypeWithValueLabels()
		
	data = {"now":now
			, "dtStart":dtStart
			, "dtEnd":dtEnd
			}
	pagedata["content"]["graphs"] = renderGraphs(self, data)
	pagedata["forms"]["graphs"] = renderGraphsForm(self, data)
	
	data = {"now":now, "statuses":getStatuses()}
	pagedata["content"]["statuses"] = renderStatuses(self, data)
	
	pagedata["forms"]["statuses"] = renderStatusesForm(self)
	
	if block=='iodevices':
		pagedata["forms"]["iodevice"] = renderIODeviceForm(self, iodevices, mode, itemid)
	else:
		pagedata["forms"]["iodevice"] = renderIODeviceForm(self, iodevices)
	
	if block=='inputs':	
		pagedata["forms"]["input"] = renderInputForm(self, inputs, mode, itemid)
	else:
		pagedata["forms"]["input"] = renderInputForm(self, inputs)
	
	if block=='outputs':
		pagedata["forms"]["output"] = renderOutputForm(self, outputs, mode, itemid)
	else:
		pagedata["forms"]["output"] = renderOutputForm(self, outputs)
	
	if block=='inputtypes':
		pagedata["forms"]["inputtypes"] = renderInputTypesForm(self, inputtypes, mode, itemid, extra)
	else:
		pagedata["forms"]["inputtypes"] = renderInputTypesForm(self, inputtypes)
	
	if block=='outputtypes':
		pagedata["forms"]["outputtypes"] = renderOutputTypesForm(self, outputtypes, mode, itemid, extra)
	else:
		pagedata["forms"]["outputtypes"] = renderOutputTypesForm(self, outputtypes)
	
	if block=='graphsettings':
		pagedata["forms"]["graphsettings"] = renderGraphSettingsForm(self, None, mode, itemid)
	else:
		pagedata["forms"]["graphsettings"] = renderGraphSettingsForm(self)
		
	if block=='rules':
		pagedata["forms"]["rules"] = renderRulesForm(self, None, mode, itemid)
	else:
		pagedata["forms"]["rules"] = renderRulesForm(self)
		
	if block=='users':
		pagedata["forms"]["users"] = renderUsersForm(self, None, mode, itemid)
	else:
		pagedata["forms"]["users"] = renderUsersForm(self)
	
	return render.index(pagedata)

def renderLoginForm(self):
	message = None
	loginform = web.form.Form(web.form.Hidden('command', value='login')
					, web.form.Textbox('login_username', description='Username')
					, web.form.Password('login_password', description='Password')
					, web.form.Button('login_submit',html="Login")
					)
	return loginform.render()
					
def renderRulesForm(self, rules=None, mode='view', itemid=None):
	message = None
	rulesform = web.form.Form(web.form.Hidden('command', value='rules')
					, web.form.Button('rule_add',html="<img src='static/add.gif'>")
					)
	
	if rules==None:
		rules = getRules()
	
	sourceoptions = [('input','input'),('output','output')]
	operationoptions = [('==','=='),('<','<'),('>','>'),('<=','<='),('>=','>='),('!=','!=')]
	comparetypeoptions = [('input','input'),('output','output'),('value','value')]
	
	outputoptions = [(0,'---')]
	for output in getOutputs():
		outputoptions.append((output['id'],output['label']))
		
	inputoptions = [(0,'---')]
	for input in getInputs():
		inputoptions.append((input['id'],input['label']))
	
	idx = -1
	for idx,rule in enumerate(rules):
		rulesform.inputs += (web.form.Hidden('rule_id_'+str(idx), value=rule['id']),)
		rulesform.inputs += (web.form.Button('rule_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		rulesform.inputs += (web.form.Button('rule_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		rulesform.inputs += (web.form.Button('rule_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		rulesform.inputs += (web.form.Button('rule_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		#edit
		if mode=='edit' and int(itemid)==int(rule['id']):
			rulesform.inputs += (web.form.Dropdown('rule_sourcetype_'+str(idx), sourceoptions, value=rule['sourcetype']),)
			rulesform.inputs += (web.form.Dropdown('rule_sourceoutputid_'+str(idx), outputoptions, value=rule['sourceoutputid']),)
			rulesform.inputs += (web.form.Dropdown('rule_sourceinputid_'+str(idx), inputoptions, value=rule['sourceinputid']),)
			rulesform.inputs += (web.form.Dropdown('rule_operation_'+str(idx), operationoptions, value=rule['operation']),)
			rulesform.inputs += (web.form.Dropdown('rule_comparetype_'+str(idx), comparetypeoptions, value=rule['comparetype']),)
			rulesform.inputs += (web.form.Textbox('rule_comparevalue_'+str(idx), class_='number', value=rule['comparevalue']),)
			rulesform.inputs += (web.form.Dropdown('rule_compareoutputid_'+str(idx), outputoptions, value=rule['compareoutputid']),)
			rulesform.inputs += (web.form.Dropdown('rule_compareinputid_'+str(idx), inputoptions, value=rule['compareinputid']),)
			rulesform.inputs += (web.form.Dropdown('rule_outcomeid_'+str(idx), outputoptions, value=rule['outcomeid']),)
			rulesform.inputs += (web.form.Textbox('rule_outcomevalue_'+str(idx), class_='number', value=rule['outcomevalue']),)
			rulesform.inputs += (web.form.Textbox('rule_priority_'+str(idx), class_='number', value=rule['priority']),)
	
	#add
	if mode=='add':
		idx += 1	
		rulesform.inputs += (web.form.Hidden('rule_id_'+str(idx), value=''),)
		rulesform.inputs += (web.form.Button('rule_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		rulesform.inputs += (web.form.Button('rule_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		rulesform.inputs += (web.form.Dropdown('rule_sourcetype_'+str(idx), sourceoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_sourceoutputid_'+str(idx), outputoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_sourceinputid_'+str(idx), inputoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_operation_'+str(idx), operationoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_comparetype_'+str(idx), comparetypeoptions, value=''),)
		rulesform.inputs += (web.form.Textbox('rule_comparevalue_'+str(idx), class_='number', value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_compareoutputid_'+str(idx), outputoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_compareinputid_'+str(idx), inputoptions, value=''),)
		rulesform.inputs += (web.form.Dropdown('rule_outcomeid_'+str(idx), outputoptions, value=''),)
		rulesform.inputs += (web.form.Textbox('rule_outcomevalue_'+str(idx), class_='number', value=''),)
		rulesform.inputs += (web.form.Textbox('rule_priority_'+str(idx), class_='number', value=''),)
	
	# form elements for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove Rule id #"+str(itemid)+"?"
		rulesform.inputs += (web.form.Button('rule_confirm_yes', html="Yes", value='yes'),)
		rulesform.inputs += (web.form.Button('rule_confirm_no', html="No", value='no'),)
		rulesform.inputs += (web.form.Hidden('rule_confirm_action', value=mode),)
		rulesform.inputs += (web.form.Hidden('rule_confirm_itemid', value=itemid),)
	
	return render.rulesform(rulesform, rules, mode, itemid, message)
	
def renderUsersForm(self, users=None, mode='view', itemid=None):
	message = None
	usersform = web.form.Form(web.form.Hidden('command', value='users')
								, web.form.Button('user_add',html="<img src='static/add.gif'>")
								)
								
	if users==None:
		users = getUsers()
	idx = -1
	for idx,user in enumerate(users):
		usersform.inputs += (web.form.Hidden('user_id_'+str(idx), value=user['id']),)
		usersform.inputs += (web.form.Button('user_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		usersform.inputs += (web.form.Button('user_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		usersform.inputs += (web.form.Button('user_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		usersform.inputs += (web.form.Button('user_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		usersform.inputs += (web.form.Textbox('user_username_'+str(idx), value=user['username']),)
		usersform.inputs += (web.form.Password('user_password_'+str(idx), value=''),)
	
	#add
	if mode=='add':
		idx += 1
		usersform.inputs += (web.form.Hidden('user_id_'+str(idx), value=''),)
		usersform.inputs += (web.form.Button('user_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		usersform.inputs += (web.form.Button('user_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		usersform.inputs += (web.form.Textbox('user_username_'+str(idx), value=''),)
		usersform.inputs += (web.form.Password('user_password_'+str(idx), value=''),)
	
	# form elements for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove User id #"+str(itemid)+"?"
		usersform.inputs += (web.form.Button('user_confirm_yes', html="Yes", value='yes'),)
		usersform.inputs += (web.form.Button('user_confirm_no', html="No", value='no'),)
		usersform.inputs += (web.form.Hidden('user_confirm_action', value=mode),)
		usersform.inputs += (web.form.Hidden('user_confirm_itemid', value=itemid),)
	
	return render.usersform(usersform, users, mode, itemid, message)

def renderGraphsForm(self, data):
	graphsform = web.form.Form(
			web.form.Hidden('command', value='getgraphs')
			, web.form.Dropdown('graphsrange'
				, ["---","1","2","4","8","12","24","36","48","72"]
				, web.form.notnull
				, description="Range:"
				)
			, web.form.Textbox('startDateTime', web.form.notnull, description="Start:", value=data['dtStart'].strftime("%Y-%m-%d %H:%M:%S"))
			, web.form.Textbox('endDateTime', web.form.notnull, description="End:", value=data['dtEnd'].strftime("%Y-%m-%d %H:%M:%S"))
			, web.form.Button('btngetgraphs',html="Get Graphs")
			, web.form.Checkbox('graphsautoupdate', value='true')
			, web.form.Textbox('graphsgetinterval', value='60000', class_='number')
			)
	return render.graphsform(graphsform)

def renderGraphSettingsForm(self, graphs=None, mode='view', itemid=None):
	message = None
	graphsettingsform = web.form.Form(web.form.Hidden('command', value='graphsettings')
					, web.form.Button('graph_add',html="<img src='static/add.gif'>")
					)
					
	if graphs==None:
		graphs = getGraphs()
	
	graphsettingsform.inputs += (web.form.Hidden('itemid', value=itemid),)
	
	iooptions = [('input','input'),('output','output')]
	
	results = db.select('input_data_type', what='id, label')
	inputdatatypes = [(0,'')]
	for idt in results:
		inputdatatypes.append((idt['id'], idt['label']))
	idx = -1
	for idx,graph in enumerate(graphs):
		graphsettingsform.inputs += (web.form.Hidden('graph_id_'+str(idx), value=graph['id']),)
		graphsettingsform.inputs += (web.form.Button('graph_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		graphsettingsform.inputs += (web.form.Button('graph_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		graphsettingsform.inputs += (web.form.Button('graph_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		graphsettingsform.inputs += (web.form.Button('graph_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		graphsettingsform.inputs += (web.form.Textbox('graph_label_'+str(idx), class_='text', value=graph['label']),)
		graphsettingsform.inputs += (web.form.Dropdown('graph_inputdatatypeid_'+str(idx), inputdatatypes, value=graph['inputdatatypeid']),)
		graphsettingsform.inputs += (web.form.Dropdown('graph_io_'+str(idx), iooptions, value=graph['io']),)
			
		#edit
		if mode=='edit' and int(itemid)==int(graph['id']):
			graph['entries'] = getGraphEntries(itemid, graph['io'])
			usedentries = []
			for idx,e in enumerate(graph['entries']):
				usedentries.append(e['ioid'])
			
			graphsettingsform.inputs += (web.form.Button('remove_entry', value='', html="<img src='static/delete.gif'>"),)
			
				
			if graph['io'] == 'input':
				data = getInputs()
			elif graph['io'] == 'output':
				data = getOutputs()
			entryoptions = [('','---')]
			for i in data:
				if usedentries.count(i['id']) == 0:
					entryoptions.append((i['id'],i['label']))
			
			graphsettingsform.inputs += (web.form.Dropdown('graph_entry', entryoptions, value=''),)
			graphsettingsform.inputs += (web.form.Button('add_entry', value=itemid, html="<img src='static/add.gif'>"),)
			
	#add
	if mode=='add':
		idx += 1
		graphsettingsform.inputs += (web.form.Hidden('graph_id_'+str(idx), value=''),)
		graphsettingsform.inputs += (web.form.Button('graph_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		graphsettingsform.inputs += (web.form.Button('graph_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		graphsettingsform.inputs += (web.form.Textbox('graph_label_'+str(idx), class_='text', value=''),)
		graphsettingsform.inputs += (web.form.Dropdown('graph_inputdatatypeid_'+str(idx), inputdatatypes, value=''),)
		graphsettingsform.inputs += (web.form.Dropdown('graph_io_'+str(idx), iooptions, value=''),)
	
	# form elements for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove Graph id #"+str(itemid)+"?"
		graphsettingsform.inputs += (web.form.Button('graph_confirm_yes', html="Yes", value='yes'),)
		graphsettingsform.inputs += (web.form.Button('graph_confirm_no', html="No", value='no'),)
		graphsettingsform.inputs += (web.form.Hidden('graph_confirm_action', value=mode),)
		graphsettingsform.inputs += (web.form.Hidden('graph_confirm_itemid', value=itemid),)
	
	return render.graphsettings(graphsettingsform, graphs, mode, itemid, message)						
	
def renderGraphs(self, data):
	data['graphs'] = list(db.select('graph'))
	for graph in data['graphs']:
		fig = plt.figure()
		
		if graph['io'] == 'input':
			inputdatatype = list(db.select('input_data_type', where='id=$id',vars={'id':graph['inputdatatypeid']}))[0]
			ylabel = inputdatatype['label'].title()+' ('+inputdatatype['unit']+')'
			
			graph_entries = list(db.select('graph_entries',what='ioid',where='graphid=$graphid', vars={'graphid':graph['id']}))
			for entry in graph_entries:
				input = list(db.select('input', where = 'id=$id', vars={'id':entry['ioid']}))[0]
				inputdata = getInputData(data['dtStart'], data['dtEnd'], entry['ioid'], graph['inputdatatypeid'])
				xs = []
				ys = []
				for d in inputdata:
					xs.append(d['datetime'])
					ys.append(d['data'])
				plt.plot(xs, ys, c=input["color"], label=input["label"])
				
		elif graph['io'] == 'output':
			ylabel = 'Output'
			
			ylim_min = 0.0
			ylim_max = 1.0
			graph_entries = list(db.select('graph_entries',what='ioid',where='graphid=$graphid', vars={'graphid':graph['id']}))
			for entry in graph_entries:
				output = list(db.select('output', where = 'id=$id', vars={'id':entry['ioid']}))[0]
				
				outputtype = getOutputTypes(id=output['outputtypeid'])[0]
				diff = (outputtype['rangeend']-outputtype['rangebegin'])*0.10
				
				if (outputtype['rangebegin']-diff) < ylim_min:
					ylim_min = outputtype['rangebegin']-diff
				if (outputtype['rangeend']+diff) > ylim_max:
					ylim_max = outputtype['rangeend']+diff
					
				outputdata = getOutputData(data['dtStart'], data['dtEnd'], entry['ioid'])
				xs = []
				ys = []
				for d in outputdata:
					xs.append(d['datetime'])
					ys.append(d['data'])
				plt.plot(xs, ys, c=output["color"], label=output["label"])
			
			plt.ylim([ylim_min,ylim_max])
			
		plt.legend(bbox_to_anchor=(1.11, 1), loc=1, borderaxespad=0.,prop={'size':6})
		fig.autofmt_xdate()
		plt.ylabel(ylabel)
		plt.savefig(os.path.join(curdir,'static/'+graph['label']+'.png'), bbox_inches='tight')
				
	return render.graphs(data)

def renderStatuses(self, data):
	return render.statuses(data)

def renderStatusesForm(self):
	refreshstatusesform = web.form.Form(web.form.Hidden('command', value="refreshstatuses")
										, web.form.Button('btnrefreshstatuses',html='Refresh')
										)
	return refreshstatusesform.render()
	
def renderIODeviceForm(self, iodevices, mode='view', itemid=None):
	message = None
	iodeviceform = web.form.Form(web.form.Hidden('command', value='iodevices')
								, web.form.Button('iodevice_add',html="<img src='static/add.gif'>")
								)
	for idx,iodevice in enumerate(iodevices):
		iodeviceform.inputs += (web.form.Hidden('iodevice_id_'+str(idx), value=iodevice['id']),)
		iodeviceform.inputs += (web.form.Button('iodevice_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		iodeviceform.inputs += (web.form.Button('iodevice_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		iodeviceform.inputs += (web.form.Button('iodevice_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		iodeviceform.inputs += (web.form.Button('iodevice_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		iodeviceform.inputs += (web.form.Textbox('iodevice_label_'+str(idx), class_='text', value=iodevice['label']),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_port_'+str(idx), class_='number', value=iodevice['port']),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_timeout_'+str(idx), class_='number', value=iodevice['timeout']),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_baud_'+str(idx), class_='number', value=iodevice['baud']),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_samplerate_'+str(idx), class_='number', value=iodevice['samplerate']),)
	
	#add
	if mode=='add':
		idx += 1
		iodeviceform.inputs += (web.form.Hidden('iodevice_id_'+str(idx), value=''),)
		iodeviceform.inputs += (web.form.Button('iodevice_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		iodeviceform.inputs += (web.form.Button('iodevice_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		iodeviceform.inputs += (web.form.Textbox('iodevice_label_'+str(idx), class_='text', value=''),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_port_'+str(idx), class_='number', value=''),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_timeout_'+str(idx), class_='number', value=''),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_baud_'+str(idx), class_='number', value=''),)
		iodeviceform.inputs += (web.form.Textbox('iodevice_samplerate_'+str(idx), class_='number', value=''),)
	
	# form elements for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove IO Device id #"+str(itemid)+"?"
		iodeviceform.inputs += (web.form.Button('iodevice_confirm_yes', html="Yes", value='yes'),)
		iodeviceform.inputs += (web.form.Button('iodevice_confirm_no', html="No", value='no'),)
		iodeviceform.inputs += (web.form.Hidden('iodevice_confirm_action', value=mode),)
		iodeviceform.inputs += (web.form.Hidden('iodevice_confirm_itemid', value=itemid),)
	
	return render.iodeviceform(iodeviceform, iodevices, mode, itemid, message)
		
def renderInputForm(self, inputs, mode='view', itemid=None):
	message = None
	inputform = web.form.Form(web.form.Hidden('command', value='inputs')
							, web.form.Button('input_add', html="<img src='static/add.gif'>")
							)
							
	#get iodevices
	results = db.select('io_device', what='id, label')
	iodevices = []
	for iodev in results:
		iodevices.append((iodev['id'], iodev['label']))
	
	#get input types
	results = db.select('input_type', what='id, name')
	types = []
	for t in results:
		types.append((t['id'],t['name']))

	
	for idx,input in enumerate(inputs):
		inputform.inputs += (web.form.Hidden('input_id_'+str(idx), value=input['id']),)
		inputform.inputs += (web.form.Button('input_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		inputform.inputs += (web.form.Button('input_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		inputform.inputs += (web.form.Button('input_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		inputform.inputs += (web.form.Button('input_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		inputform.inputs += (web.form.Dropdown('input_iodevice_'+str(idx), iodevices, value=input['iodeviceid']),)
		inputform.inputs += (web.form.Dropdown('input_type_'+str(idx), types, value=input['inputtypeid']),)
		inputform.inputs += (web.form.Textbox('input_label_'+str(idx), class_='text', value=input['label']),)
		inputform.inputs += (web.form.Textbox('input_color_'+str(idx), class_='color', value=input['color']),)
		inputform.inputs += (web.form.Textbox('input_pin_'+str(idx), class_='number', value=input['pin']),)
		
	#add
	if mode=='add':
		idx += 1
		inputform.inputs += (web.form.Hidden('input_id_'+str(idx), value=''),)
		inputform.inputs += (web.form.Button('input_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		inputform.inputs += (web.form.Button('input_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		inputform.inputs += (web.form.Dropdown('input_iodevice_'+str(idx), iodevices, value=''),)
		inputform.inputs += (web.form.Dropdown('input_type_'+str(idx), types, value=''),)
		inputform.inputs += (web.form.Textbox('input_label_'+str(idx), class_='text', value=''),)
		inputform.inputs += (web.form.Textbox('input_color_'+str(idx), class_='color', value=''),)
		inputform.inputs += (web.form.Textbox('input_pin_'+str(idx), class_='number', value=''),)
	
	# form elements for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove Input id #"+str(itemid)+"?"
		inputform.inputs += (web.form.Button('input_confirm_yes', html="Yes", value='yes'),)
		inputform.inputs += (web.form.Button('input_confirm_no', html="No", value='no'),)
		inputform.inputs += (web.form.Hidden('input_confirm_action', value=mode),)
		inputform.inputs += (web.form.Hidden('input_confirm_itemid', value=itemid),)
		
	return render.inputform(inputform, inputs, mode, itemid, message)

def renderInputTypesForm(self, inputtypes, mode='view', itemid=None, extra=None):
	message = None
	
	#form elements for every row grouping in all modes
	inputtypesform = web.form.Form(web.form.Hidden('command', value='inputtypes')
					, web.form.Button('inputtype_add', html="<img src='static/add.gif'", value="add")
					)
	previd = 0; idx = 0; group = -1
	for inputtype in inputtypes:
		if previd != inputtype['id']:
			if extra != None and int(itemid)==int(previd):
				inputtypesform.inputs += (web.form.Hidden('inputtype_idtid_'+str(group)+'_'+str(idx), web.form.notnull, value=''),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_label_'+str(group)+'_'+str(idx), class_='text', value=''),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_unit_'+str(group)+'_'+str(idx), class_='text', value=''),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_rangebegin_'+str(group)+'_'+str(idx), class_='number', value=''),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_rangeend_'+str(group)+'_'+str(idx), class_='number', value=''),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_accuracy_'+str(group)+'_'+str(idx), class_='number', value=''),)
			idx = 0; group += 1
			inputtypesform.inputs += (web.form.Button('inputtype_remove_'+str(group), html="<img src='static/delete.gif'>", value='remove'),)
			inputtypesform.inputs += (web.form.Button('inputtype_edit_'+str(group), html="<img src='static/edit.gif'>", value='edit'),)
			inputtypesform.inputs += (web.form.Hidden('inputtype_id_'+str(group), value=inputtype['id']),)
		inputtypesform.inputs += (web.form.Hidden('inputtype_idtid_'+str(group)+'_'+str(idx), web.form.notnull, value=inputtype['idtid']),)
		previd = inputtype['id']
		idx += 1
	if extra != None and int(itemid)==int(previd):
		inputtypesform.inputs += (web.form.Hidden('inputtype_idtid_'+str(group)+'_'+str(idx), web.form.notnull, value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_label_'+str(group)+'_'+str(idx), class_='text', value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_unit_'+str(group)+'_'+str(idx), class_='text', value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_rangebegin_'+str(group)+'_'+str(idx), class_='number', value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_rangeend_'+str(group)+'_'+str(idx), class_='number', value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_accuracy_'+str(group)+'_'+str(idx), class_='number', value=''),)
		
	#form elements for edit mode
	if mode=='edit':
		previd = 0; idx = -1; group = -1
		for inputtype in inputtypes:
			idx += 1
			if previd != inputtype['id']:
				idx = 0; group += 1
				if itemid==inputtype['id']:
					inputtypesform.inputs += (web.form.Button('inputtype_cancel_'+str(group), html="<img src='static/cancel.gif'>", value='cancel'),)
					inputtypesform.inputs += (web.form.Button('inputtype_adddatatype_'+str(group), html="<img src='static/add.gif'> Data Type", value='adddatatype'),)
					inputtypesform.inputs += (web.form.Button('inputtype_save_'+str(group), html="<img src='static/save.gif'>", value='save'),)
					inputtypesform.inputs += (web.form.Textbox('inputtype_name_'+str(group), class_='text', value=inputtype['name']),)
					inputtypesform.inputs += (web.form.Textbox('inputtype_maxsamplerate_'+str(group), class_='number', value=inputtype['maxsamplerate']),)
			if itemid==inputtype['id']:
				inputtypesform.inputs += (web.form.Textbox('inputtype_label_'+str(group)+'_'+str(idx), class_='text', value=inputtype['label']),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_unit_'+str(group)+'_'+str(idx), class_='text', value=inputtype['unit']),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_rangebegin_'+str(group)+'_'+str(idx), class_='number', value=inputtype['rangebegin']),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_rangeend_'+str(group)+'_'+str(idx), class_='number', value=inputtype['rangeend']),)
				inputtypesform.inputs += (web.form.Textbox('inputtype_accuracy_'+str(group)+'_'+str(idx), class_='number', value=inputtype['accuracy']),)
			previd = inputtype['id']
			
	#form elements for add mode
	if mode == 'add':
		group += 1
		inputtypesform.inputs += (web.form.Button('inputtype_cancel_'+str(group), html="<img src='static/cancel.gif'>", value='cancel'),)
		inputtypesform.inputs += (web.form.Button('inputtype_save_'+str(group), html="<img src='static/save.gif'>", value='save'),)
		inputtypesform.inputs += (web.form.Hidden('inputtype_id_'+str(group), value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_name_'+str(group), class_='text', value=''),)
		inputtypesform.inputs += (web.form.Textbox('inputtype_maxsamplerate_'+str(group), class_='number', value=''),)
	
	# form element for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove id #"+str(itemid)+" and all it's data types?"
		inputtypesform.inputs += (web.form.Button('inputtype_confirm_yes', html="Yes", value='yes'),)
		inputtypesform.inputs += (web.form.Button('inputtype_confirm_no', html="No", value='no'),)
		inputtypesform.inputs += (web.form.Hidden('inputtype_confirm_action', value=mode),)
		inputtypesform.inputs += (web.form.Hidden('inputtype_confirm_itemid', value=itemid),)
					
	return render.inputtypesform(inputtypesform, inputtypes, mode, itemid, extra, message)

def renderOutputForm(self, outputs, mode='view', itemid=None):
	message = None
	outputform = web.form.Form(web.form.Hidden('command', value='outputs')
							, web.form.Button('output_add', html="<img src='static/add.gif'>")
							)
							
	#get iodevices
	results = db.select('io_device', what='id, label')
	iodevices = []
	for iodev in results:
		iodevices.append((iodev['id'], iodev['label']))
	
	#get output types
	results = db.select('output_type', what='id, name')
	types = []
	for t in results:
		types.append((t['id'],t['name']))
		
	for idx,output in enumerate(outputs):
		outputform.inputs += (web.form.Hidden('output_id_'+str(idx), value=output['id']),)
		outputform.inputs += (web.form.Button('output_edit_'+str(idx), value='edit', html="<img src='static/edit.gif'>"),)
		outputform.inputs += (web.form.Button('output_remove_'+str(idx), value='remove', html="<img src='static/delete.gif'>"),)
		outputform.inputs += (web.form.Button('output_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		outputform.inputs += (web.form.Button('output_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		outputform.inputs += (web.form.Dropdown('output_iodevice_'+str(idx), iodevices, value=output['iodeviceid']),)
		outputform.inputs += (web.form.Dropdown('output_type_'+str(idx), types, value=output['outputtypeid']),)
		outputform.inputs += (web.form.Textbox('output_label_'+str(idx), class_='text', value=output['label']),)
		outputform.inputs += (web.form.Textbox('output_color_'+str(idx), class_='color', value=output['color']),)
		outputform.inputs += (web.form.Textbox('output_defaultvalue_'+str(idx), class_='number', value=output['defaultvalue']),)
		outputform.inputs += (web.form.Textbox('output_pin_'+str(idx), class_='number', value=output['pin']),)
	
	#add
	if mode=='add':
		idx += 1
		outputform.inputs += (web.form.Hidden('output_id_'+str(idx), value=''),)
		outputform.inputs += (web.form.Button('output_cancel_'+str(idx), value='cancel', html="<img src='static/cancel.gif'>"),)
		outputform.inputs += (web.form.Button('output_save_'+str(idx), value='save', html="<img src='static/save.gif'>"),)
		
		outputform.inputs += (web.form.Dropdown('output_iodevice_'+str(idx), iodevices, value=''),)
		outputform.inputs += (web.form.Dropdown('output_type_'+str(idx), types, value=''),)
		outputform.inputs += (web.form.Textbox('output_label_'+str(idx), class_='text', value=''),)
		outputform.inputs += (web.form.Textbox('output_color_'+str(idx), class_='color', value=''),)
		outputform.inputs += (web.form.Textbox('output_defaultvalue_'+str(idx), class_='number', value=''),)
		outputform.inputs += (web.form.Textbox('output_pin_'+str(idx), class_='number', value=''),)
	
	# form element for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove Output id #"+str(itemid)+"?"
		outputform.inputs += (web.form.Button('output_confirm_yes', html="Yes", value='yes'),)
		outputform.inputs += (web.form.Button('output_confirm_no', html="No", value='no'),)
		outputform.inputs += (web.form.Hidden('output_confirm_action', value=mode),)
		outputform.inputs += (web.form.Hidden('output_confirm_itemid', value=itemid),)
	
	return render.outputform(outputform, outputs, mode, itemid, message)

def renderOutputTypesForm(self, outputtypes, mode='view', itemid=None, extra=None):
	message = None
	
	#form elements for every row grouping in all modes
	outputtypesform = web.form.Form(web.form.Hidden('command', value='outputtypes')
								, web.form.Button('outputtype_add', html="<img src='static/add.gif'>", value='add')
								)
	previd = 0; idx = 0; group = -1
	for outputtype in outputtypes:
		if previd != outputtype['id']:
			if extra != None and int(itemid)==int(previd):
				outputtypesform.inputs += (web.form.Hidden('outputtype_ovlid_'+str(group)+'_'+str(idx), web.form.notnull, value=''),)
				outputtypesform.inputs += (web.form.Textbox('outputtype_label_'+str(group)+'_'+str(idx), class_='text', value=''),)
				outputtypesform.inputs += (web.form.Textbox('outputtype_value_'+str(group)+'_'+str(idx), class_='number', value=''),)
			idx = 0; group += 1
			outputtypesform.inputs += (web.form.Button('outputtype_remove_'+str(group), html="<img src='static/delete.gif'>", value='remove'),)
			outputtypesform.inputs += (web.form.Button('outputtype_edit_'+str(group), html="<img src='static/edit.gif'>", value='edit'),)
			outputtypesform.inputs += (web.form.Hidden('outputtype_id_'+str(group), value=outputtype['id']),)
		outputtypesform.inputs += (web.form.Hidden('outputtype_ovlid_'+str(group)+'_'+str(idx), web.form.notnull, value=outputtype['ovlid']),)
		previd = outputtype['id']
		idx += 1
	if extra != None and int(itemid)==int(previd):
		outputtypesform.inputs += (web.form.Hidden('outputtype_ovlid_'+str(group)+'_'+str(idx), web.form.notnull, value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_label_'+str(group)+'_'+str(idx), class_='text', value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_value_'+str(group)+'_'+str(idx), class_='number', value=''),)
		
	#form elements for edit mode
	if mode=='edit':
		previd = 0; idx = -1; group = -1
		for outputtype in outputtypes:
			idx += 1
			if previd != outputtype['id']:
				idx = 0; group += 1
				if itemid==outputtype['id']:
					outputtypesform.inputs += (web.form.Button('outputtype_cancel_'+str(group), html="<img src='static/cancel.gif'>", value='cancel'),)
					outputtypesform.inputs += (web.form.Button('outputtype_addvaluelabel_'+str(group), html="<img src='static/add.gif'> Label", value='addvaluelabel'),)
					outputtypesform.inputs += (web.form.Button('outputtype_save_'+str(group), html="<img src='static/save.gif'>", value='save'),)
					outputtypesform.inputs += (web.form.Textbox('outputtype_name_'+str(group), class_='text', value=outputtype['name']),)
					outputtypesform.inputs += (web.form.Textbox('outputtype_rangebegin_'+str(group), class_='number', value=outputtype['rangebegin']),)
					outputtypesform.inputs += (web.form.Textbox('outputtype_rangeend_'+str(group), class_='number', value=outputtype['rangeend']),)
					outputtypesform.inputs += (web.form.Textbox('outputtype_maxupdaterate_'+str(group), class_='number', value=outputtype['maxupdaterate']),)
			if itemid==outputtype['id']:
				outputtypesform.inputs += (web.form.Textbox('outputtype_label_'+str(group)+'_'+str(idx), class_='text', value=outputtype['label']),)
				outputtypesform.inputs += (web.form.Textbox('outputtype_value_'+str(group)+'_'+str(idx), class_='number', value=outputtype['value']),)
			previd = outputtype['id']
			
			

	
	#form elements for add mode
	if mode == 'add':
		group += 1
		outputtypesform.inputs += (web.form.Button('outputtype_cancel_'+str(group), html="<img src='static/cancel.gif'>", value='cancel'),)
		outputtypesform.inputs += (web.form.Button('outputtype_save_'+str(group), html="<img src='static/save.gif'>", value='save'),)
		outputtypesform.inputs += (web.form.Hidden('outputtype_id_'+str(group), value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_name_'+str(group), class_='text', value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_rangebegin_'+str(group), class_='number', value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_rangeend_'+str(group), class_='number', value=''),)
		outputtypesform.inputs += (web.form.Textbox('outputtype_maxupdaterate_'+str(group), class_='number', value=''),)
	
	# form element for remove mode
	if mode == 'remove':
		message = "Are you sure you want to remove id #"+str(itemid)+" and all it's value labels?"
		outputtypesform.inputs += (web.form.Button('outputtype_confirm_yes', html="Yes", value='yes'),)
		outputtypesform.inputs += (web.form.Button('outputtype_confirm_no', html="No", value='no'),)
		outputtypesform.inputs += (web.form.Hidden('outputtype_confirm_action', value=mode),)
		outputtypesform.inputs += (web.form.Hidden('outputtype_confirm_itemid', value=itemid),)
					
	return render.outputtypesform(outputtypesform, outputtypes, mode, itemid, extra, message)
	
def renderOutcome(self, message):
	return render.saveoutcome(message)
	
	
#---------------------------------------------------------------------
# GETS / LOADS
#---------------------------------------------------------------------	

def getStatuses():
	ret = {}
	#for every input and output fetch the most recent record from the DB
	
	ret["inputs"] = []
	allinputtypes = getInputTypes();
	for it in allinputtypes:
		inputtype = {'name':it.name}
		inputtype['inputs'] = []
		
		inputdatatypes = getInputDataTypes(inputtypeid=it.id)
		inputtype['datatypes'] = []
		for dt in inputdatatypes:
			datatype = {'label':dt.label,'unit':dt.unit}
			inputtype['datatypes'].append(datatype)
		
		inputs = getInputs(inputtypeid=it.id, orderby='label')
		for input in inputs:
			data = {'label':input.label}
			for dt in inputdatatypes:
				#GET THE DATA
				sql = "SELECT data, datetime"
				sql+= " FROM input_data"
				sql+= " WHERE datatypeid=$datatypeid"
				sql+= "   AND inputid=$inputid"
				sql+= " ORDER BY datetime DESC"
				sql+= " LIMIT 1"
				vars = {'datatypeid':dt.id,'inputid':input.id}
				result = db.query(sql, vars=vars)
				if len(result)>0:
					data[dt.label] = result[0]
				else:
					data[dt.label] = {'data':'---','datetime':'---'}
			inputtype['inputs'].append(data)
		
		ret["inputs"].append(inputtype)
	
	
	outputs = getOutputs()
	ret["outputs"] = []
	for output in outputs:
		sql = "SELECT D.outputid"
		sql+= " , D.data"
		sql+= " , D.datetime"
		sql+= " , O.label"
		sql+= " , O.color"
		sql+= " , OVL.label as datalabel"
		sql+= "	FROM output_data D"
		sql+= " JOIN output O"
		sql+= "   ON O.id = D.outputid"
		sql+= " LEFT JOIN output_value_labels OVL"
		sql+= "   ON OVL.outputtypeid = D.outputid"
		sql+= "   AND OVL.value = D.data"
		sql+= " WHERE D.outputid = $outputid"
		sql+= " ORDER BY d.datetime DESC"
		sql+= " LIMIT 1"
		results = db.query(sql,vars={'outputid':output['id']})
		if len(results) > 0:
			o = results[0]
			ret['outputs'].append({"data":o['data']
				,"datalabel":o['datalabel']
				,"datetime":o['datetime']
				,"label":o['label']
				,"color":o['color']
				})
		else:
			ret['outputs'].append({"data":"---"
				,"datalabel":''
				,"datetime":''
				,"label":output['label']
				,"color":''
				})
	
	return ret

def getInputData(dtStart, dtEnd, inputid=None, datatypeid=None):
	where = "datetime >= $start AND datetime <= $end"
	vars = {'start':dtStart.strftime("%Y-%m-%d %H:%M:%S"), 'end':dtEnd.strftime("%Y-%m-%d %H:%M:%S")}
	
	if inputid != None:
		where += " AND inputid=$inputid"
		vars['inputid'] = inputid
		
	if datatypeid != None:
		where += " AND datatypeid=$datatypeid"
		vars['datatypeid'] = datatypeid
	
	results = db.select('input_data'
		, what = "inputid, datatypeid, data, datetime"
		, where = where
		, vars = vars
		, order="datetime ASC")
	return results
	
def getOutputData(dtStart, dtEnd, outputid=None):
	where = ("datetime >= '"+dtStart.strftime("%Y-%m-%d %H:%M:%S")+"'"
		+" AND datetime <= '"+dtEnd.strftime("%Y-%m-%d %H:%M:%S")+"'")		
	
	vars = {}
	if outputid != None:
		where += " AND outputid=$outputid"
		vars['outputid'] = outputid
		
	results = db.select('output_data'
		, what = "outputid,data,datetime"
		, where = where
		, vars = vars
		, order="datetime ASC")
	return results
					
def getInputs(inputtypeid = None, orderby=None):
	vars = {}
	if inputtypeid != None:
		wheresql = ' WHERE I.inputtypeid=$inputtypeid'
		vars['inputtypeid'] = inputtypeid
	else:
		wheresql = ''
		
	if orderby != None:
		orderbysql = " ORDER BY "+orderby
	else:
		orderbysql = "";

	sql = "SELECT I.*, IT.name as type, IO.label as iodevice"
	sql+= " FROM input I"
	sql+= " JOIN input_type IT"
	sql+= "   ON IT.id = I.inputtypeid"
	sql+= " JOIN io_device IO"
	sql+= "   ON IO.id = I.iodeviceid"
	sql+= wheresql
	sql+= orderbysql
	orderby
	return list(db.query(sql, vars=vars))

def getOutputs():
	sql = "SELECT O.*, OT.name as type, IO.label as iodevice"
	sql+= " FROM output O"
	sql+= " JOIN output_type OT"
	sql+= "   ON OT.id = O.outputtypeid"
	sql+= " JOIN io_device IO"
	sql+= "   ON IO.id = O.iodeviceid"
	sql+= " ORDER BY O.outputtypeid, O.label"
	return list(db.query(sql))

def getOutputTypes(id=None):
	where = None
	vars = None
	if id != None:
		where = " id=$id"
		vars = {'id':id}
	
	return list(db.select('output_type', where=where, vars=vars))
	
def getInputTypes():
	return list(db.select('input_type'))
		
def getInputDataTypes(inputtypeid = None):
	where = None
	vars = None
	if inputtypeid != None:
		where = " inputtypeid=$inputtypeid"
		vars = {'inputtypeid':inputtypeid}
	result = db.select('input_data_type', where=where, vars=vars)
	return list(result)
	
def getIODevices():
	return list(db.select('io_device'))

def getRules():
	sql = "SELECT R.*"
	sql+= ", SI.label as silabel, SO.label as solabel"
	sql+= ", CI.label as cilabel, CO.label as colabel"
	sql+= ", O.label as olabel"
	sql+= " FROM rule R"
	sql+= " LEFT JOIN input SI"
	sql+= "   ON SI.id = R.sourceinputid"
	sql+= " LEFT JOIN output SO"
	sql+= "   ON SO.id = R.sourceoutputid"
	sql+= " LEFT JOIN input CI"
	sql+= "   ON CI.id = R.compareinputid"
	sql+= " LEFT JOIN output CO"
	sql+= "   ON CO.id = R.compareoutputid"
	sql+= " LEFT JOIN output O"
	sql+= "   ON O.id = R.outcomeid"
	sql+= " ORDER BY R.priority ASC"
	return list(db.query(sql))
	
def getInputTypeWithDataTypes(id = None):
	sql = "SELECT IT.*"
	sql+= ", IDT.id as idtid"
	sql+= ", IDT.label"
	sql+= ", IDT.unit"
	sql+= ", IDT.rangebegin"
	sql+= ", IDT.rangeend"
	sql+= ", IDT.accuracy"
	sql+= " FROM input_type IT"
	sql+= " LEFT JOIN input_data_type IDT"
	sql+= "   ON IDT.inputtypeid = IT.id"
	vars = {}
	if id != None:
		sql+= " WHERE IT.id = $id"
		vars["id"] = id
	sql+= " ORDER BY IT.id ASC, IDT.id ASC"
	return list(db.query(sql, vars))

def getOutputTypeWithValueLabels(id = None):
	sql = "SELECT OT.*"
	sql+= ", OVL.id as ovlid"
	sql+= ", OVL.label"
	sql+= ", OVL.value"
	sql+= " FROM output_type OT"
	sql+= " LEFT JOIN output_value_labels OVL"
	sql+= "   ON OVL.outputtypeid = OT.id"
	vars = {}
	if id != None:
		sql+= " WHERE OT.id = $id"
		vars["id"] = id
	sql+= " ORDER BY OT.id, OVL.value"
	return list(db.query(sql, vars))

def getGraphs():
	sql = "SELECT G.*, IDT.label as inputdatatype"
	sql+= " FROM graph G"
	sql+= " LEFT JOIN input_data_type IDT"
	sql+= "   ON IDT.id = G.inputdatatypeid"
	return list(db.query(sql))

def getGraphEntries(graphid, io):
	sql = "SELECT GE.id, GE.ioid, IO.label"
	sql+= " FROM graph_entries GE"
	if io=='input':
		sql+= " JOIN input IO"
		sql+= "   ON IO.id = GE.ioid"
	elif io=='output':
		sql+= " JOIN output IO"
		sql+= "   ON IO.id = GE.ioid"
	sql+= " WHERE GE.graphid=$graphid"
	sql+= " ORDER BY IO.label ASC"
	return list(db.query(sql, vars={'graphid':graphid}))

def getUsers():
	return list(db.select('cism_users'))
	
	
#---------------------------------------------------------------------	
# SAVES
#---------------------------------------------------------------------

def saveGraph(f, i):
	id = getattr(f,"graph_id_"+str(i))
	label = getattr(f,"graph_label_"+str(i))
	inputdatatypeid = getattr(f,"graph_inputdatatypeid_"+str(i))
	io = getattr(f,"graph_io_"+str(i))
	if id != '':
		db.update('graph'
				, label = label
				, inputdatatypeid = inputdatatypeid
				, io = io
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('graph'
				, label = label
				, inputdatatypeid = inputdatatypeid
				, io = io
				)
	return
	
def saveIODevice(f, i):
	id = getattr(f,"iodevice_id_"+str(i))
	label = getattr(f, "iodevice_label_"+str(i))
	port = getattr(f, "iodevice_port_"+str(i))
	timeout = getattr(f, "iodevice_timeout_"+str(i))
	baud = getattr(f, "iodevice_baud_"+str(i))
	samplerate = getattr(f, "iodevice_samplerate_"+str(i))
	if id != '':
		db.update('io_device'
				, label = label
				, port = port
				, timeout = timeout
				, baud = baud
				, samplerate = samplerate
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('io_device'
				, label = label
				, port = port
				, timeout = timeout
				, baud = baud
				, samplerate = samplerate
				)
	return
	
def saveRule(f, i):
	id = getattr(f,"rule_id_"+str(i))
	
	sourcetype = getattr(f, "rule_sourcetype_"+str(i))
	sourceoutputid = getattr(f, "rule_sourceoutputid_"+str(i))
	sourceinputid = getattr(f, "rule_sourceinputid_"+str(i))
	operation = getattr(f, "rule_operation_"+str(i))
	comparetype = getattr(f, "rule_comparetype_"+str(i))
	comparevalue = getattr(f, "rule_comparevalue_"+str(i))
	compareoutputid = getattr(f, "rule_compareoutputid_"+str(i))
	compareinputid = getattr(f, "rule_compareinputid_"+str(i))
	outcomeid = getattr(f, "rule_outcomeid_"+str(i))
	outcomevalue = getattr(f, "rule_outcomevalue_"+str(i))
	priority = getattr(f, "rule_priority_"+str(i))
	
	if id != '':
		db.update('rule'
				, sourcetype = sourcetype
				, sourceoutputid = sourceoutputid
				, sourceinputid = sourceinputid
				, operation = operation
				, comparetype = comparetype
				, comparevalue = comparevalue
				, compareoutputid = compareoutputid
				, compareinputid = compareinputid
				, outcomeid = outcomeid
				, outcomevalue = outcomevalue
				, priority = priority
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('rule'
				, sourcetype = sourcetype
				, sourceoutputid = sourceoutputid
				, sourceinputid = sourceinputid
				, operation = operation
				, comparetype = comparetype
				, comparevalue = comparevalue
				, compareoutputid = compareoutputid
				, compareinputid = compareinputid
				, outcomeid = outcomeid
				, outcomevalue = outcomevalue
				, priority = priority
				)
	return
	
def saveInput(f, i):
	id = getattr(f,"input_id_"+str(i))
	iodeviceid = getattr(f, "input_iodevice_"+str(i))
	inputtypeid = getattr(f, "input_type_"+str(i))
	pin = getattr(f, "input_pin_"+str(i))
	label = getattr(f, "input_label_"+str(i))
	color = getattr(f, "input_color_"+str(i))
	if id != '':
		db.update('input'
				, iodeviceid = iodeviceid
				, pin = pin
				, inputtypeid = inputtypeid
				, label = label
				, color = color
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('input'
				, iodeviceid = iodeviceid
				, pin = pin
				, inputtypeid = inputtypeid
				, label = label
				, color = color
				)
	return

def saveOutput(f, i):
	id = getattr(f,"output_id_"+str(i))
	iodeviceid = getattr(f, "output_iodevice_"+str(i))
	outputtypeid = getattr(f, "output_type_"+str(i))
	pin = getattr(f, "output_pin_"+str(i))
	label = getattr(f, "output_label_"+str(i))
	color = getattr(f, "output_color_"+str(i))
	if id != '':
		db.update('output'
				, iodeviceid = iodeviceid
				, pin = pin
				, outputtypeid = outputtypeid
				, label = label
				, color = color
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('output'
				, iodeviceid = iodeviceid
				, pin = pin
				, outputtypeid = outputtypeid
				, label = label
				, color = color
				)
	return
	
def saveOutputType(f, i):
	
	id = getattr(f,"outputtype_id_"+str(i))
	name = getattr(f,"outputtype_name_"+str(i))
	rangebegin = getattr(f,"outputtype_rangebegin_"+str(i))
	rangeend = getattr(f,"outputtype_rangeend_"+str(i))
	maxupdaterate = getattr(f,"outputtype_maxupdaterate_"+str(i))
	if id != '':
		db.update('output_type'
				, name = name
				, rangebegin = rangebegin
				, rangeend = rangeend
				, maxupdaterate = maxupdaterate
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('output_type'
				, name = name
				, rangebegin = rangebegin
				, rangeend = rangeend
				, maxupdaterate = maxupdaterate
				)
	return
	
def saveOutputValueLabels(f, g):
	id = getattr(f,"outputtype_id_"+str(g))
	otwvls = getOutputTypeWithValueLabels(id=id)
	# update or add value labels
	for i in range(0, len(otwvls)+1):
		if isset(f, "outputtype_ovlid_"+str(g)+"_"+str(i)):
			ovlid = getattr(f,"outputtype_ovlid_"+str(g)+"_"+str(i))
			label = getattr(f,"outputtype_label_"+str(g)+"_"+str(i))
			value = getattr(f,"outputtype_value_"+str(g)+"_"+str(i))
			if label!='' and value!='':
				if ovlid != '':
					db.update('output_value_labels'
						, label = label
						, value = value
						, where = "id = $id"
						, vars = {"id":ovlid}
						)
				else:
					db.insert('output_value_labels'
						, label = label
						, value = value
						, outputtypeid = id
						)		
	return

def saveInputType(f, i):
	id = getattr(f,"inputtype_id_"+str(i))
	name = getattr(f,"inputtype_name_"+str(i))
	maxsamplerate = getattr(f,"inputtype_maxsamplerate_"+str(i))
	if id != '':
		db.update('input_type'
				, name = name
				, maxsamplerate = maxsamplerate
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('input_type'
				, name = name
				, maxsamplerate = maxsamplerate
				)
	return
	
def saveInputDataTypes(f, g):
	id = getattr(f,"inputtype_id_"+str(g))
	itwdts = getInputTypeWithDataTypes(id=id)
	# update or add data types
	for i in range(0, len(itwdts)+1):
		if isset(f, "inputtype_idtid_"+str(g)+"_"+str(i)):
			idtid = getattr(f,"inputtype_idtid_"+str(g)+"_"+str(i))
			label = getattr(f,"inputtype_label_"+str(g)+"_"+str(i))
			unit = getattr(f,"inputtype_unit_"+str(g)+"_"+str(i))
			rangebegin = getattr(f,"inputtype_rangebegin_"+str(g)+"_"+str(i))
			rangeend = getattr(f,"inputtype_rangeend_"+str(g)+"_"+str(i))
			accuracy = getattr(f,"inputtype_accuracy_"+str(g)+"_"+str(i))
			if label!='' and unit!='' and rangebegin!='' and rangeend!='' and accuracy!='':
				if idtid != '':
					db.update('input_data_type'
						, label = label
						, unit = unit
						, rangebegin = rangebegin
						, rangeend = rangeend
						, accuracy = accuracy
						, where = "id = $id"
						, vars = {"id":idtid}
						)
				else:
					db.insert('input_data_type'
						, label = label
						, unit = unit
						, rangebegin = rangebegin
						, rangeend = rangeend
						, accuracy = accuracy
						, inputtypeid = id
						)		
	return
	
def saveUser(f, i):
	id = getattr(f,"user_id_"+str(i))
	username = getattr(f, "user_username_"+str(i))
	password = getattr(f, "user_password_"+str(i))
	pwdhash = hashlib.md5(username+password).hexdigest()
	if id != '':
		db.update('cism_users'
				, username = username
				, password = pwdhash
				, where = "id = $id"
				, vars = {'id':id}
				)
	else:
		db.insert('cism_users'
				, username = username
				, password = pwdhash
				)
	return
	
#---------------------------------------------------------------------	
# Support Utilities
#---------------------------------------------------------------------

def isRenderWholePageOff(f):
	try:
		if int(f.rwp)==0: #Render Whole Page Off
			return True
		else:
			return False
	except AttributeError:
		return False

def isset(f, attr):
	try:
		getattr(f, attr)
		return True
	except AttributeError:
		return False

	