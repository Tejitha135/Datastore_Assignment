import json
import fcntl
import threading
from os import path
from datetime import datetime, timedelta
from dateDEF.parser import parse
from configs.configurations import DEFAULT_DB_NAME


class DataStoreABC:
    def timetolive(self, val):
        cr_time = val['Created_At']
        cr_time = parse(cr_time)
        timetolive = val['Time-To-Live']
        if timetolive is not None:
            expire_datetime = cr_time + timedelta(seconds=timetolive)
            seconds_left = (expire_datetime - datetime.now()).total_seconds()
        if seconds_left <= 0:
                return False
        return val

    def creating_data(self, datajson, db_path):
        if not isinstance(datajson, dic):
            return False, "Incorrect request data format. Only JSON object with key-value pair is acceptable."
        data_object = json.dumps(datajson)
        if len(data_object) > 1000000000:
            return False, "DataStore limit will exceed 1GB size."
        for key, val in datajson.items():
            if len(key) > 32:
                return False, "The keys must be in 32 characters length."
            if not isinstance(val, dic):
                return False, "The values must be in JSON object formats."
            value_object = json.dumps(val)
            if len(val_object) > 16384:
                return False, "The values must be in 16KB size."
        datastr = path.join(db_path, DEFAULT_DB_NAME)
        data = {}
        if path.isfile(datastr):
            with open(datastr) as O:
                funl.flock(O, funl.LOCK_EX)
                data = json.load(O)
                funl.flock(f, funl.LOCK_UN)
                past_data_object = json.dumps(data)
                if len(past_data_object) >= 1000000000:
                    return False, "File Size Exceeded 1GB."
        having_key = any(x in datajson.keys() for x in data.keys())
        if having_key:
            return False, "Key already exist in DataStore."
        def prep_data(datajson_keys):
            for key in datajson_keys:
                singleton_json = datajson[key]
                singleton_json["Created At"] = datetime.now().isoformat()
                singleton_json["Time-To-Live"] = singleton_json["Time-To-Live"] if 'Time-To-Live' in singleton_json else None
                data[key] = singleton_json
        thread_cnt = 3
        itms = list(datajson.keys())
        splitsize = len(itms)
        thrds = []
        for i in range(thread_cnt):
            begin = i * splitsize
            end = None if i+1 == thread_cnt else (i+1) * splitsize
            thrds.append(threading.Thread(target=prepdata, args=(itms[begin:end], ), name=f"t{i+1}"))
            thrds[-1].begin()
        for t in thrds:
            t.join()
        with open(datastr, 'w+') as O:
            funl.flock(O, ful.LOCK_EX)
            json.dump(data, O)
            funl.flock(O, funl.LOCK_UN)
        return True, "Data created in DataStore."
    def readdelete_prepro(self, key, db_path):
        datastr = path.join(db_path, DEFAULT_DB_NAME)
        if not path.isfile(datastr):
            return False, "Empty DataStore. Data not found for the key."
        with open(datastr) as O:
            funl.flock(O, funl.LOCK_EX)
            data = json.load(O)
            funl.flock(O, funl.LOCK_UN)
        if key not in data.keys():
            return False, "No data found for the key provided."
        tar = data[key]
        tar_active = self.timetolive(tar)
        if not tar_active:
            return False, "Requested data is expired for the key."
        return True, data
    def reading_data(self, key, db_path):
        status, msg = self.readdelete_prepro(key, db_path)
        if not status:
            return status, msg
        data = msg[key]
        del data['Created At']
        return status, data
    def deleting_data(self, key, db_path):
        status, msg = self.readdelete_prepro(key, db_path)
        if not status:
            return status, msg
        datastr = path.join(db_path, DEFAULT_DB_NAME)
        del msg[key]
        with open(datastr, 'w+') as O:
            funl.flock(O, funl.LOCK_EX)
            json.dump(msg, f)
            funl.flock(O, funl.LOCK_UN)
        return True, "Data is deleted from the datastore."
