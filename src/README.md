## Files

Here are the essential files needed for this proejct:

* Main.py: a Python script that calculates the top x customers with the highest Simple Lifetime Value from data D
* input.txt: input files containing events data
* output.txt : output files with customer id and its Lifetime Value

Use command `python Main.py` to run the program

## Approach

After reading in the event data line by line, I created a dict with customer_id as the key and its corresponding events as the value. The tricky part is to calculate the number of weeks for timeframe from the given data. When an order or a site visit event occurs, their event times are added to a list. The start and the end of the time frame are the mininum and the maximum value of this list respectively. For example, user A might visit shufferfly on Jan 1st, and this user's last visit or order placement might be Mar 1st. Between Jan 1st and Mar 1st, user A might or might not be placing orders in shutterfly. If user A does not place orders within this time frame, then the average value of user A's expenditure would be lowered comapred to other users who are continuously placing orders wihtin the same time frame.

I notice in the event data, type "Order" has two actions for verb, "New" and "Update". My understanding on "Update" is that, for example, if the user decides to add "print 10 more pictures" service on top of the previous order, then this newer event would update the event time and the total amount spent for this particular order. So in the code, if the order id is found in the existing order information, then the newer order information will overwrite the old one.

Overall, this code challenge is a great case study exercise allowing me to understand the business metric, user behavior and corner case analysis. 