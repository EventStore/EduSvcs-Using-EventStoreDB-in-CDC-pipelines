from esdbclient import EventStoreDBClient, NewEvent, StreamState

#########
# Enabling $by_correlation_id projections allows 
# A client to read all the changes caused by a transaction
#########

# Create a client
client = EventStoreDBClient(uri="esdb://localhost:2113?tls=false")


# Note the setting resolve_links, events in a projection are links to the 
# original event in other languages besides python the setting is resolveLinkTos = True
# The by correlation_id projection projects events with matching correlation ID's in the Event's 
# metadata to a stream

# Note you will have to replace the stream_name here with 
# a value from a multi-row operation. 
# the sql folder has an add_customers script that adds 5 customers in one transaction
# use the correlation ID from one of the per row events

######
# Events generated by the intial snapshot have a correlationID of None
# This is used as the default for this demo, because it will work
# To show events for a transaction, run some of the SQL scripts
# View an event, copy the correlationID value from the events metadata
# and replace "None" with that correlationID
# it will resemble "0b267379-6678-11ef-b939-0242ac110004:175"
###########

correlationID = "None" # Replace with your correlationID
stream_name = f"$bc-{correlationID}"

try:
    events = client.get_stream(stream_name, resolve_links=True)


    for event in events:
        print(f" \n {event.type}")
        print(event.data)

    print("success")
except:
    print("No Such Stream \n Are projections Enabled? \n Did you enter a valid correlationID?")    
client.close()