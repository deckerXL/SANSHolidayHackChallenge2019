from datetime import datetime
from calendar import timegm
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--year", help="4 digit Year {2019}", required=True)
parser.add_argument("--month", help="2 digit Year {12}", required=True)
parser.add_argument("--day", help="2 digit Day {25}", required=True)
parser.add_argument("--hour", help="2 digit hour in military time {19}", required=True)
parser.add_argument("--minutes", help="2 digit minutes in military time {00}", required=True)
parser.add_argument("--seconds", help="2 digit minutes in military time {00}", required=True)
args = parser.parse_args()

# Note: if you pass in a naive dttm object it's assumed to already be in UTC
def unix_time(dttm=None):
    if dttm is None:
       dttm = datetime.utcnow()

    return timegm(dttm.utctimetuple())

print ("Unix Epoch UTC timestamp for "+str(args.month)+"/"+str(args.day)+"/"+str(args.year)+" "+str(args.hour)+":"+str(args.minutes)+":"+str(args.seconds)+\
	" = "+str(unix_time(datetime(int(args.year), int(args.month), int(args.day), int(args.hour), int(args.minutes), int(args.seconds)))))
