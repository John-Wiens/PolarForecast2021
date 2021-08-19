import json
import datetime
import time
import TBA

if(TBA.check_connection()):
    raw_events, is_updated = TBA.get('/events/2021')
    for event in raw_events:
        if event['event_code'] == 'isjo':
            print(event)


        
    