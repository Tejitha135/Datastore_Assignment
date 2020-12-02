from sys import exit
from argparse import ArgumentParser
from configs import configurations
from DEF.filehandler import FilePro
from ABC.functions import DataStoreCRD


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
''' Reading data '''
data_found, msg= DataStoreABC().reading_data(key, db_path)
print(msg)

