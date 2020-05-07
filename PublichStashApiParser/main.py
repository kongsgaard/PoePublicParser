from logger import get_logger
from publicStashApi import PublicStashApi
from mongodbPersist import MongoDbPersist
import optparse

def parse_arguments():
    parser = optparse.OptionParser()

    parser.add_option('-l', '--dblink', default='mongodb://mongo')
    parser.add_option('-d', '--database', default='PoePublicStash')
    parser.add_option('-c', '--dbcollection', default='RawFetches')
    parser.add_option('-p', '--dbport', default=27017)

    options, args = parser.parse_args()

    return options, args

if __name__ == '__main__':
    mylogger = get_logger()

    options, args = parse_arguments()

    p = PublicStashApi(rate_limit_seconds=2, logger=mylogger)
    mongo = MongoDbPersist(options.dblink,options.dbport,options.database,options.dbcollection,mylogger)

    for i in range(0, 25):
        fetch_data = p.get_next_id()
        mongo.persist_json(fetch_data)