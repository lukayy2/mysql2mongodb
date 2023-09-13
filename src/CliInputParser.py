import configparser
import argparse
import os
import sys


class CliInputParser:

    def parse(self):
        # configure from args
        if len(sys.argv) > 1:
            parser = argparse.ArgumentParser()

            parser.add_argument("--mysqlHost", help="Mysql(Source) Hostname or IP", required=True)
            parser.add_argument("--mysqlUser", help="Mysql(Source) Usernmae", required=True)
            parser.add_argument("--mysqlPassword", help="Mysql(Source) Password", required=True)
            parser.add_argument("--mysqlDatabase", help="Mysql(Source) Database", required=True)
            parser.add_argument("--mysqlTable", help="Mysql(Source) Table", required=True)

            parser.add_argument("--mongoHost", help="MongoDB(Dest) Hostname or IP", required=True)
            parser.add_argument("--mongoUser", help="MongoDB(Dest) Username", required=True)
            parser.add_argument("--mongoPassword", help="MongoDB(Dest) Password", required=True)
            parser.add_argument("--mongoDatabase", help="MongoDB(Dest) Database", required=True)
            parser.add_argument("--mongoCollection", help="MongoDB(Dest) Collection", required=True)

            parser.add_argument("--selectlimit",
                                help="Rows to select at once (Tweak for best Performance) Default: 100", type=int, default=100)

            args = parser.parse_args()

            return self.__convertArgsToDict(args)

        else:
            # confiure from config.ini
            if not os.path.exists('config.ini'):
                raise RuntimeError('no config.ini presend in Directory!')

            config = configparser.ConfigParser()
            config.read('config.ini')


            return config

    def __convertArgsToDict(self, args):
        dictConfig = {}
        dictConfig['default'] = {}
        dictConfig['mysql'] = {}
        dictConfig['mongodb'] = {}

        dictConfig['default']['selectlimit'] = args.selectlimit

        dictConfig['mysql']['host'] = args.mysqlHost
        dictConfig['mysql']['user'] = args.mysqlUser
        dictConfig['mysql']['password'] = args.mysqlPassword
        dictConfig['mysql']['database'] = args.mysqlDatabase
        dictConfig['mysql']['table'] = args.mysqlTable

        dictConfig['mongodb']['host'] = args.mongoHost
        dictConfig['mongodb']['user'] = args.mongoUser
        dictConfig['mongodb']['password'] = args.mongoPassword
        dictConfig['mongodb']['database'] = args.mongoDatabase
        dictConfig['mongodb']['collection'] = args.mongoCollection

        return dictConfig