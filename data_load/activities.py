import pandas as pd
import json

from util.vdot import daniels_vdot
from data_load.common import DATA_DIR

ID_COLUMNS = [
    'Activity Date', 'Activity Name', 'Activity Type',
       'Activity Description', 'Filename', 'Start Time', 
]


NUM_COLUMNS = [
    'Elapsed Time', 'Distance', 'Max Heart Rate',
       'Moving Time', 'Max Speed', 'Average Speed',
       'Elevation Gain', 'Elevation Loss', 'Elevation Low', 'Elevation High',
       'Max Grade', 'Average Grade', 'Average Positive Grade',
       'Average Negative Grade', 'Max Cadence', 'Average Cadence',
       'Average Heart Rate', 'Max Watts', 'Average Watts',
       'Calories',
]

def load_race_distance_corrections():
    with open(DATA_DIR / 'race_distance_corrections.json', 'r') as f:
        corrections = json.load(f)
    return corrections

def fill_dates(activities: pd.DataFrame):
    # take a dataframe with missing dates and fill in rows of nans for missing dates
    dates = pd.date_range(activities['Activity Date'].min(), activities['Activity Date'].max(), freq='D')
    all_dates = pd.DataFrame(dates, columns=['Activity Date'])
    all_dates['Activity Date'] = pd.to_datetime(all_dates['Activity Date']).dt.date
    return all_dates.merge(activities, on='Activity Date', how='left')

def compute_cumulative_miles(activities: pd.DataFrame):
    mileage = activities[['Activity Date', 'Distance']].copy().set_index('Activity Date')
    
    activities['Cumulative Mileage (7D)'] = mileage.rolling('7D').sum().values
    activities['Cumulative Mileage (30D)'] = mileage.rolling('30D').sum().values
    activities['Cumulative Mileage (365D)'] = mileage.rolling('365D').sum().values
    return activities

def populate_vdot(activities: pd.DataFrame):
    aux = activities.copy()
    aux['time_minutes'] = aux['Elapsed Time'] / 60
    aux['distance_meters'] = aux['Distance'] * 1609.34
    activities['VDOT Effective'] = aux.apply(lambda x: daniels_vdot(x['time_minutes'], x['distance_meters']), axis=1)
    return activities

def load_activities():
    activities = pd.read_csv(DATA_DIR / 'activities.csv', index_col=0)
    activities = activities.loc[activities['Activity Type'] == 'Run'].copy()
    activities[NUM_COLUMNS] = activities[NUM_COLUMNS].apply(pd.to_numeric)
    activities['Distance'] = activities['Distance'] / 1.60934 # convert to miles
    # apply a correction to botched GPS race distances
    corrections = load_race_distance_corrections()
    for key, value in corrections.items():
        activities.loc[int(key), 'Distance'] = value
    pace_decimal_minutes = activities['Elapsed Time'] / activities['Distance'] / 60
    activities['Average Pace'] = pace_decimal_minutes.apply(lambda x: f"{int(x)}:{int((x - int(x)) * 60):02d}")
    num_columns = NUM_COLUMNS + ['Average Pace']
    
    # activities['Activity Time'] = pd.to_datetime(activities['Activity Date']).dt.time
    # activities['Activity Date'] = pd.to_datetime(activities['Activity Date']).dt.date
    # activities = activities.sort_values(['Activity Date', 'Activity Time'])
    # activities = fill_dates(activities)
    activities['Activity Date'] = pd.to_datetime(activities['Activity Date'])
    activities = activities.sort_values('Activity Date')
    activities = compute_cumulative_miles(activities)
    num_columns += ['Cumulative Mileage (7D)', 'Cumulative Mileage (30D)', 'Cumulative Mileage (365D)']
    activities = populate_vdot(activities)
    num_columns += ['VDOT Effective']
    return activities[ID_COLUMNS + num_columns]

if __name__ == "__main__":
    activities = load_activities()
    print(activities.columns)
    print(activities[['Activity Date', 'Distance', 'Cumulative Mileage (7D)']].head(10).values)
    print(activities.loc[12847840012, "Activity Description"])
    
    print(activities.sort_values('VDOT Effective', ascending=False)[['Activity Date', 'Activity Name', 'Distance', 'Average Pace', 'VDOT Effective']].head(30))
    print(activities.sort_values('VDOT Effective', ascending=True)[['Activity Date', 'Activity Name', 'Distance', 'Average Pace']].head(10))