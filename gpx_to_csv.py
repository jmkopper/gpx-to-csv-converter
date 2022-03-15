import re
from datetime import datetime
import csv

GPX_FILENAME = "GPX_FILENAME_HERE.gpx"
CSV_FILENAME = "CSV_FILENAME_HERE.csv"

lats = []
longs = []
eles = []
times = []
distance = []

gpx_file = open(GPX_FILENAME, 'r')
lines = gpx_file.readlines()[5:]  # Skip some metadata

for line in lines:
    lats += re.findall(r'lat="(.*?)"', line)
    longs += re.findall(r'lon="(.*?)"', line)
    eles += re.findall(r'<ele>(.*?)</ele>', line)
    time_raw = re.findall(r'<time>(.*?)Z</time>', line)
    if time_raw:
        times.append(
            datetime.strptime(time_raw[0], '%Y-%m-%dT%H:%M:%S'))  # gpx times are formatted yyyy-mm-ddT00:00:00Z
    distance += re.findall(r'<distance>(.*?)</distance>', line)

gpx_file.close()

# Compute time deltas
time_deltas = [0]
elapsed_times = [0]

for i in range(1, len(times)):
    time_deltas.append((times[i] - times[i - 1]).total_seconds())
    elapsed_times.append((times[i] - times[0]).total_seconds())

fields = {'Latitude': lats, 'Longitude': longs, 'Elevation': eles, 'Time': times, 'Distance': distance,
          'Time Delta': time_deltas, 'Time Elapsed': elapsed_times}

# Protect against devices that don't record all stats, e.g., elevation
good_fields = [x for x in fields.keys() if fields[x]]
good_rows = [fields[x] for x in good_fields]
rows = zip(*good_rows)

with open(CSV_FILENAME, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(good_fields)
    csvwriter.writerows(rows)
