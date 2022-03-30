import asyncio
import time

from sense_hat import SenseHat
from siridb.connector import SiriDBClient


async def collect_data(siri):

    # Start connecting to SiriDB.
    await siri.connect()

    # Initialize the Raspberry Pi Sense HAT.
    sense = SenseHat()

    try:
        # Make sure the script runs indefinitely.
        while True:

            # Get the current temperature and round it to 2 decimal places.
            temp = round(sense.get_temperature(), 2)

            # Get the current humidity and round it to 2 decimal places.
            humi = round(sense.get_humidity(), 2)

            # Get the current pressure and round it to 2 decimal places.
            pres = round(sense.get_pressure(), 2)

            # Show the current temperature on the Sense HAT.
            sense.show_message('%s C' % temp)

            # Get the current time in seconds since the Epoch.
            ts = int(time.time())

            # Add the collected data to the SiriDB serie: "temperature".
            await siri.insert({'temperature': [[ts, temp]]})

            # Add the collected data to the SiriDB serie: "humidity".
            await siri.insert({'humidity': [[ts, humi]]})

            # Add the collected data to the SiriDB serie: "pressure".
            await siri.insert({'pressure': [[ts, pres]]})

            # Wait 10 seconds before retrieving new measurements.
            await asyncio.sleep(10)

    finally:
        # Close all SiriDB connections.
        siri.close()

# Initialize the SiriDB client.
siri = SiriDBClient(
    username='iris', # Default username
    password='siri', # Default password
    dbname='iot', # The name of the database we created earlier
    hostlist=[('localhost', 9000)],  # Multiple connections are supported
    keepalive=True 
)

loop = asyncio.get_event_loop()
loop.run_until_complete(collect_data(siri))
