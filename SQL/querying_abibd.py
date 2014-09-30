__author__ = 'swei'
import sys
import pg
import time
ticks=time.clock()

try:
    con = pg.connect(dbname='abidb', host=None, user='swei', port=5434, passwd='cloudy14')
    results = con.query(
    "select  period_dttm,site_id,nee_f, ppfd_f" +
    "  from vw_fluxnet " +
    " where period_dttm between '1-jan-2004 00:00' and '5-jan-2004 23:59' " +
    " order by  site_id, period_dttm")
    # for row in results.getresult():
    #     print row
    for row in results.dictresult():
        # print "site_id=", row["site_id"]
        # print "period_dttm=", row['period_dttm']
        # print "nee=", row["nee_f"]
        print row['site_id'],row['period_dttm'],row['nee_f'],row['ppfd_f']
except:
    print "Unexpected error:", sys.exc_info()[0]
else:
    print "done with no exceptions"

print time.clock()-ticks
