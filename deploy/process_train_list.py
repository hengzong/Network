import json
import urllib.parse
import urllib.request
import urllib
import http
import time
import sys
import datetime

train_dates = {
    'C1': '2020-10-07', 
    'C2': '2020-10-07', 
    'C3': '2020-10-07', 
    'C5': '2020-10-07', 
    'C6': '2020-10-07', 
    'C7': '2020-10-06', 
    'C8': '2020-10-07', 
    'C9': '2020-10-07', 
    'D0': '2020-10-09', 
    'D1': '2020-10-09', 
    'D2': '2020-10-07', 
    'D3': '2020-10-07', 
    'D4': '2020-10-07', 
    'D5': '2020-10-07', 
    'D6': '2020-10-07', 
    'D7': '2020-10-06', 
    'D8': '2020-10-06', 
    'D9': '2020-10-07', 
    'G1': '2020-10-06',
    'G2': '2020-10-06',
    'G3': '2020-10-06',
    'G4': '2020-10-06',
    'G5': '2020-10-06',
    'G6': '2020-10-06',
    'G7': '2020-10-06',
    'G8': '2020-10-06',
    'G9': '2020-10-06' 
}

files = {
    './datasets/C/C1_trains.json': '2020-10-07', 
    './datasets/C/C2_trains.json': '2020-10-07', 
    './datasets/C/C3_trains.json': '2020-10-07', 
    './datasets/C/C5_trains.json': '2020-10-07',
    './datasets/C/C6_trains.json': '2020-10-07',
    './datasets/C/C7_trains.json': '2020-10-06',
    './datasets/C/C8_trains.json': '2020-10-07',
    './datasets/C/C9_trains.json': '2020-10-07',
    './datasets/D/D0_trains.json': '2020-10-09',
    './datasets/D/D1_trains.json': '2020-10-09',
    './datasets/D/D2_trains.json': '2020-10-07',
    './datasets/D/D3_trains.json': '2020-10-07',
    './datasets/D/D4_trains.json': '2020-10-07',
    './datasets/D/D5_trains.json': '2020-10-07',
    './datasets/D/D6_trains.json': '2020-10-07',
    './datasets/D/D7_trains.json': '2020-10-06',
    './datasets/D/D8_trains.json': '2020-10-06',
    './datasets/D/D9_trains.json': '2020-10-07',
    './datasets/G/G1_trains.json': '2020-10-06',
    './datasets/G/G2_trains.json': '2020-10-06',
    './datasets/G/G3_trains.json': '2020-10-06',
    './datasets/G/G4_trains.json': '2020-10-06',
    './datasets/G/G5_trains.json': '2020-10-06',
    './datasets/G/G6_trains.json': '2020-10-06',
    './datasets/G/G7_trains.json': '2020-10-06',
    './datasets/G/G8_trains.json': '2020-10-06',
    './datasets/G/G9_trains.json': '2020-10-06',
}

def getSchedule(train_no, train_date):
    url = 'https://kyfw.12306.cn/otn/queryTrainInfo/query?leftTicketDTO.train_no=' + train_no + '&leftTicketDTO.train_date=' + train_date + '&rand_code='
    try:
        with urllib.request.urlopen(url) as response:
            res = response.read().decode("utf8", 'ignore')
            data = json.loads(res)['data']
            return data['data']

    except (urllib.error.URLError, http.client.HTTPException, OSError) as e: 
        print('------------------')
        print(train_no, train_date)
        print(e)
        return []    

if __name__ == "__main__":
    fp = sys.argv[1]
    train_date = files[fp]

    schedules = {}
    errors = []
    with open(fp) as f:
        start = datetime.datetime.now()
        trains = json.load(f)['data']
        n_trains = len(trains)
        for i, t in enumerate(trains):
            train_no = t['train_no']
            train_code = t['station_train_code']
            # print(str(i) + '/' + str(n_trains) + ' Getting ' + train_no)
            schedules[train_no] = getSchedule(train_no, train_date)
            if len(schedules[train_no]) == 0:
                errors.append((train_no, train_code))
            time.sleep(0.01)
    
        # print('Retraining errors')
        errors_copy = errors.copy()
        n_trains = len(errors_copy)
        for i, t in enumerate(errors_copy):
            train_no, train_code = t
            # print(str(i) + '/' + str(n_trains) + ' Getting ' + train_no)
            schedules[train_no] = {
                'schedule': getSchedule(train_no, train_date),
                'train_code': train_code
            }
            time.sleep(0.01)
        # print(schedules)
        end = datetime.datetime.now()
        print(fp + " Used Time: " + str(end-start))

    outfile = fp.replace('datasets', 'outfiles')
    with open(outfile, 'w', encoding='utf8') as outfile:
        json.dump(schedules, outfile, ensure_ascii=False)
    





