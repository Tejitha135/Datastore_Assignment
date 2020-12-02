from sys import exit
from utils.filehandler import FilePreprocess
#from ABC.functions import DataStoreABC
from argparse import ArgumentParser
from configs import configurations

parse = ArgumentParser()
parse.add_argument('--datastore', help='Enter the datastore absolute path.')
args = parse.parse_args()
if args.datastr:
    db_path = args.datr
else:
    db_path = configurations.DEFAULT_DB_PATH
dir_created = FilePreprocess(db_path).create_folder()
if not dir_created:
    print(f"Permission denied: You can not create the directory `{db_path}`.\n")
    exit(0)
datajson= {
    "abc": {
        "data1": "value1",
        "data2": "value2",
        "data3": "value3",
        "Time-To-Live": 5000,
    },
    "def": {
        "data1": "value1",
        "data2": "value2",
        "data3": "value3",
        "Time-To-Live": 50,
    },
    "ghi": {
        "data1": "value1",
        "data2": "value2",
        "data3": "value3",
        "data4": "value4",
    },
    "jkl": {
        "data1": "value1",
        "data2": "value2",
        "data3": "value3",
        "Time-To-Live": 250,
    }
}
''' Creating data '''
valid_data, msg = DataStoreABC().creating_data(datajson, db_path)
print(msg)

