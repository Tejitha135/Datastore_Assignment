from sys import exit
from argparse import ArgumentParser
from configs import settings, configurations
from DEF.filehandler import FilePreprocess
from ABC.functions import DataStoreABC

parse = ArgumentParser()
parse.add_argument('--datastore', help='Enter the datastore absolute path.')
args = parse.parse_args()
if args.datastr:
    db_path = args.datastr
else:
    db_path = configurations.DEFAULT_DB_PATH
dir_created = FilePro(db_path).create_file()
if not dir_created:
    print(f"Permission denied: You can not create the directory `{db_path}`.\n")
    exit(0)
key = 'ghi'
'''deleting data '''
data_found, msg = DataStoreABC().deleting_data(key, db_path)
print(msg)

