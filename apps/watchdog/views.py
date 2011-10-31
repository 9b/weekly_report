#report IDs 
def check_report_id(id):
	check_result = False #assume we always fail first
	if len(id) != 16:
		return check_result
	
	if isinstance(id,int):
		return check_result
	
	check_result = True #made it without returning
	return check_result
	
def check_report_date(date):
	check_result = False
	parts = date.split("/")
	
	if len(parts) != 3:
		return check_result
	
	for part in parts:
		try:
			part = int(part)
		except:
			return check_result
			
		if not isinstance(part,int):
			return check_result
			
	check_result = True
	return check_result