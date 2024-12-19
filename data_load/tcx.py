import pathlib

import pandas as pd


DATA_DIR = pathlib.Path(__file__).parent.parent / 'sample_data' / 'export_32380589'

def pace_to_decimal(pace: str):
    try:
        return float(pace.split(':')[0]) + float(pace.split(':')[1])/60.
    except:
        return None

def tcx_to_dataframe(file):
    with open(file, 'r') as f:
        data = f.read()
        
    data = data.replace('\n', '').replace('\t', '')
    data = data.split('<Trackpoint>')
    data = data[1:]
    
    def get_value(tag, data):
        start = data.find(f'<{tag}>') + len(f'<{tag}>')
        end = data.find(f'</{tag}>', start)
        if '<Value>' in data[start:end]:
            return get_value('Value', data[start:end])
        else:
            return data[start:end]
    
    def get_values(data):
        return {
            'timestamp': get_value('Time', data),
            'position_lat': get_value('LatitudeDegrees', data),
            'position_long': get_value('LongitudeDegrees', data),
            'distance': get_value('DistanceMeters', data),
            'altitude': get_value('Elevation', data),
            'speed': get_value('Speed', data),
            'heart_rate': get_value('HeartRateBpm', data),
            'cadence': get_value('Cadence', data),
            'temperature': get_value('Temperature', data),
            'watts': get_value('Watts', data),
            'pace': get_value('Pace', data),
            'incline': get_value('Incline', data)
        }
    
    data = [get_values(d) for d in data]
    data = pd.DataFrame(data)
    data['position_lat'] = data['position_lat'].astype(float)
    data['position_long'] = data['position_long'].astype(float)
    data['distance'] = data['distance'].astype(float)
    data['altitude'] = data['altitude'].astype(float)
    data['speed'] = data['speed'].astype(float)
    data['heart_rate'] = data['heart_rate'].astype(float)
    data['cadence'] = data['cadence'].astype(float)
    data['temperature'] = data['temperature'].astype(float)
    data['watts'] = data['watts'].astype(float)
    data['timestamp'] = pd.to_datetime(data['timestamp'])
    data['pace'] = [pace_to_decimal(pace) for pace in data['pace'].values]
    data['incline'] = data['incline'].astype(float)
    
    return data

if __name__ == "__main__":
    file = DATA_DIR / 'activities' / '13773350695.tcx'
    data = tcx_to_dataframe(file)
    print(data.head(10))