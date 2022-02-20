import anomality
import events
import parser

class Event:
    def __init__(self, start_date, end_date, lat, lng, closest_airport, visitors, exhibitors, flights):
        self.start_date = start_date
        self.end_date = end_date
        self.lat = lat
        self.lng = lng
        self.closest_airport = get_closest_airport(lat, lng)
        self.flights = flights
        self.visitors = visitors
        self.exhibitors = exhibitors
        self.p = 3 * exhibitors + visitors
        self.anomality_factor = get_anomality_factor(self)

events = []

events_df = pd.read_csv(events_file)[['visitors', 'exhibitors', 'lat', 'lng', 'start_date', 'end_date']]
for i, row in events_df.iterrows():

    closest_airport = get_closest_airport(row['lat'], row['lng'])
    events_df.at[i, 'iata'] = closest_airport['iata']
    events_df.at[i, 'distance'] = closest_airport['distance']

    start_date = row['start_date']
    end_date = row['end_date']
    lat = row['lat']
    lng = row['lng']
    closest_airport = get_closest_airport(lat, lng)

    # columns to normalize
    average_columns = ['visitors', 'exhibitors']
    for column in average_columns:

        no_commas = str(row[column]).replace(',', '')
        split = re.split('\D+', no_commas)

        try:
            num_range = list(map(float, split))
            events_df.at[i, column] = np.mean(num_range)
        except:
            events_df.at[i, column] = 0

    visitors = column[0]
    exhibitors = column[1]

    event = Event(start_date, end_date, lat, lng, closest_airport, visitors, exhibitors)   
    events.append(event)

print(events)