import pathlib
from typing import List, Dict

from garmin_fit_sdk import Decoder, Stream
import pandas as pd


EPOCH_COLUMNS = ['timestamp', 'position_lat', 'position_long', 'distance', 'enhanced_altitude', 'enhanced_speed', 'heart_rate', 'cadence', 'fractional_cadence', 'temperature']

def position_to_dec_deg(position: int):
    try:
        return position / 11930465. # this is (2^32 / 360). See https://gis.stackexchange.com/questions/371656/garmin-fit-coordinate-system
    except:
        return None

def epochs_to_dataframe(epochs: List[Dict]):
    data = { col: [] for col in EPOCH_COLUMNS }
    for epoch in epochs:
        for col in EPOCH_COLUMNS:
            if col not in epoch:
                data[col].append(None)
            else:
                data[col].append(epoch[col])
                
    data['position_lat'] = [position_to_dec_deg(lat) for lat in data['position_lat']]
    data['position_long'] = [position_to_dec_deg(lon) for lon in data['position_long']]
    return pd.DataFrame(data)

def laps_to_dataframe(laps: List[Dict]):
    data = {}
    for idx, lap in enumerate(laps):
        for col in lap.keys():
            if col not in data:
                data[col] = [None] * idx
            data[col].append(lap[col])
    data['start_position_lat'] = [position_to_dec_deg(lat) for lat in data['start_position_lat']]
    data['start_position_long'] = [position_to_dec_deg(lon) for lon in data['start_position_long']]
    data['end_position_lat'] = [position_to_dec_deg(lat) for lat in data['end_position_lat']]
    data['end_position_long'] = [position_to_dec_deg(lon) for lon in data['end_position_long']]
    return pd.DataFrame(data)
    

if __name__ == '__main__':

    stream = Stream.from_file(DATA_DIR / 'activities' / '13890450040.fit')
    decoder = Decoder(stream)
    messages, errors = decoder.read()

    # print(errors)
    epochs = epochs_to_dataframe(messages['record_mesgs'])
    laps = laps_to_dataframe(messages['lap_mesgs'])
    print(epochs.columns)
    print(epochs.head(10))
    print(laps.columns)
    print(laps.head(10))