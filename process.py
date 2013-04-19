import sys, traceback, web, serial, json, time

#web.config.debug = False

db = web.database(dbn='postgres', user='swit', pw='PWtest0!', db='cism')

serconn = []
iodevice = list(db.select('io_device',what='id,label,port,baud,timeout,samplerate'))
for iodev in iodevice:
	try:
		ser = serial.Serial(iodev['port'], iodev['baud'], timeout=iodev['timeout'])
		serconn.append(ser)
	except ValueError, SerialException:
		printError("ERROR: connecting to "+iodevice[0]['port'])

def printError(msg):
	print "!!!!!!"
	print msg
	print "!!!!!!"
	serconn[0].close()
	sys.exit()
	
def process():
	now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	print "-------------------"
	print now
	print "-------------------"
	
	try:
		serconn[0].write("getjson\n")
		serialdata = serconn[0].readline()
		#print "\n_'"+serialdata+"'_"
	except ValueError, SerialException:
		printError("ERROR: getjson failed")
	
	if serialdata=='':
		print "NO_DATA"
		print "^---",now,"---"
		return
	
	try:
		data = json.loads(serialdata)
		print data
	except ValueError:
		print "\n_'"+serialdata+"'_"
		printError("ERROR: Decoding getjson JSON ")
	
	try:
		error = data['!']
	except KeyError:
		error = None
	if error is not None:
		return
	
	for input in data['input']:
		sql = "SELECT IDT.id, IDT.label"
		sql += " FROM input I"
		sql += " JOIN input_data_type IDT"
		sql += "   ON IDT.inputtypeid = I.inputtypeid"
		sql += " WHERE I.id=$id"
		inputdatatyperesults = db.query(sql, vars={'id':input['id']})
		for idt in inputdatatyperesults: 
			if input[idt['label']]!="nan":
				db.insert('input_data'
					, inputid=input['id']
					, data=input[idt['label']]
					, datatypeid=idt['id']
					, datetime=now)

	for output in data['output']:
		db.insert('output_data'
			, outputid = output['id']
			, data = output['data']
			, datetime = now)
	
	print "^---",now,"---"
	return

def main():
    try:
		print "CISM IO Process"
		print "[Ctrl-C to Exit.]"
		try:
			serialdata = serconn[0].readline()
			print serialdata
		except ValueError, SerialException:
			printError("ERROR: reading from "+iodevice[0]['port'])
		
		try:
			data = json.loads(serialdata)
			print data
		except ValueError:
			printError('ERROR: Decoding initial JSON')
			
		if data['name'] == "CISM":
		
			print "Connected to CISM v"+data['version']+" device on "+iodevice[0]['port']
		
			samplerate = iodevice[0]['samplerate']/1000

			lastlaunched = -1;
			while True:
				now = time.localtime()
				minute = now[4]
				second = now[5]
				if (lastlaunched!=minute and (minute%samplerate)==0 and second==0) or lastlaunched==-1:
					lastlaunched = minute
					results = db.select('io_device',what='samplerate',where="id="+str(iodevice[0]['id']))
					samplerate = results[0]['samplerate']/1000
					process()
				time.sleep(1)
		else:
			print "ERROR: No CISM device found on "+iodevice[0]['port']
			
    except KeyboardInterrupt:
        print "\nExiting..."
    except Exception:
        traceback.print_exc(file=sys.stdout)
		
	serconn[0].close()
    sys.exit(0)

if __name__ == "__main__":
    main()