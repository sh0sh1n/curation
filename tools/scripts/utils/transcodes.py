import psycopg2
import pandas as pd
import sys
from config import conn as c
import re

sqlQuery = "SELECT * FROM transcode LEFT JOIN asset ON (transcode.asset = asset.id);"

def makeConnection():
    try:
        conn = psycopg2.connect(dbname=c._DEV_CREDENTIALS['db'], 
                                user=c._DEV_CREDENTIALS['u'],
                                host=c._DEV_CREDENTIALS['host'],
                                password=c._DEV_CREDENTIALS['p'])
    except Exception as e:
        print("Unable to connect to database. Exception: %s" % str(e), file=sys.stderr)

    return conn.cursor()

def getData(cursor):
    try:
        cursor.execute(sqlQuery)
    except Exception as e:
        print("Query for everything failed. Exception: %s" % str(e), file=sys.stderr)
    rows = cursor.fetchall()
    return rows

def filterErrors(data:list) -> dict:
    terrors = {d[9]:[] for d in data}
    pattern = re.compile(r'\[(\w+)\s@\s\w+\](.*)')
    for d in data:
        if d[7] != None:
            loglines = d[7].split('\n')
            for line in loglines:
                m = re.match(pattern, line) 
                if m:
                    terrors[d[9]].append({'asset': d[1], 
                                          'msg_group': m.group(1).strip(), 
                                          'msg':m.group(2).strip()})
    return terrors

def filteredDataFrame(fdata:dict):
    flattened = []
    for k in fdata:
        for f in fdata[k]:
            f['vol'] = k
            flattened.append(f)
    return pd.DataFrame(flattened)


def errorsByVolume(errors):
    for k in sorted(errors):
        print("%s: %s" % (k, len(errors[k])))

def librarySummary(fd):
    pass

def errorSummary(fd):
    pass

def volumeSummar(fd):
    pass

def generateReport(filteredData:dict):
    pass



'''notes: 1) incomplete frame is followed by a new line and Error while decoding stream ??
          2) Mutiple frames in a packet from stream _ not begining with memory location
          3) what kind of reports do we need
                - aggregate '''
          