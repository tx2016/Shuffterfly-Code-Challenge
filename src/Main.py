import dateutil.parser
import json
from dateutil import rrule
from datetime import datetime, timedelta
import operator

# ref: https://stackoverflow.com/questions/14191832/how-to-calculate-difference-between-two-dates-in-weeks-in-python
def weeks_between(start_date, end_date):
	weeks = rrule.rrule(rrule.WEEKLY, dtstart = start_date, until = end_date)
	return weeks.count()

# the returned number should plus 1
# since the same week would return 0
def weeks_between2(d1, d2):
	monday1 = (d1 - timedelta(days=d1.weekday()))
	monday2 = (d2 - timedelta(days=d2.weekday()))
	return ((monday2 - monday1).days / 7)

def readin(file_dir, data):
	with open(file_dir, "r") as f:
		formatted_file = []
		for line in f:
			formatted_file.append(line.strip())
		
	# remove the "[" for the first line of information
	formatted_file[0] = formatted_file[0][1:]
	# remove the "," and "]" for the rest 
	for line in formatted_file:
		line = line[:-1]
		ingest(line, data)


def readout(file_dir, data):
	with open(file_dir, "w") as f:
		for line in data:
			f.write('{customerID: ' + line[0] + ', LTV: ' + str(line[1]) + '}' + '\n')		
	

def ingest(line, data):
	# convert each line in json format to a dictionary format
	the_dict = json.loads(line)
	# convert the format to ISO 8601 format
	the_dict['event_time'] = dateutil.parser.parse(the_dict['event_time'])

	if the_dict['type'] == "CUSTOMER":
		cusID = the_dict['key']
	else:
		cusID = the_dict['customer_id']

	if cusID in data:
		data[cusID].append(the_dict)
	else:
		data[cusID] = [the_dict]

def TopXSimpleLTVCustomers(x, data):
	# store the event time for order and site visit
	cusID_LTV = {}
	for cusID in data:
		visit_order_time = []
		order_info = {} # key: order_id, value: (event_time, total_amount)
		for event in data[cusID]:
			if event['type'] == "SITE_VISIT":
				visit_order_time.append(event['event_time'])
			elif event['type'] == "ORDER":
				visit_order_time.append(event['event_time'])
				total_amount = float(event['total_amount'].split()[0])

				if event['key'] in order_info:
					prev_event_time = order_info[event['key']][0]
					# the order has update in the verb
					# update the total amount and time if the event time is newer
					if event['event_time'] > prev_event_time:
						order_info[event['key']][0] = event['event_time']
						order_info[event['key']][1] = total_amount
				else:
					order_info[event['key']] = [event['event_time'], total_amount]

		numOfWeeks = weeks_between(min(visit_order_time), max(visit_order_time))
		# print(("numofwks is {}").format(numOfWeeks))		
		# print(order_info)
		
		sum_amount = 0
		for order_key in order_info:
			sum_amount += order_info[order_key][1]

		avg_amount = float(sum_amount) / numOfWeeks
		LTV = 520 * avg_amount
		cusID_LTV[cusID] = LTV

	# print(cusID_LTV)
	answer = sorted(cusID_LTV.iteritems(), key=operator.itemgetter(1), reverse=True)[:x]
	return answer

if __name__ == '__main__':
	input_dir = "../input/input0.txt"
	cusID_event = {} #key: customer ID, value: event associated with this customer
	readin(input_dir, cusID_event)
	result = TopXSimpleLTVCustomers(5, cusID_event)
	output_dir = "../output/output0.txt"
	readout(output_dir, result)
