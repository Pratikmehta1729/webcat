""" consist routines to fetch data from rank, keyword, size table in web.db """

from datetime import date, timedelta 
from webdata import * 
import sqlite3 


def keywords_by_cluster(cluster, date=DB_DATE, all=False, start=DB_FIRST_DATE, end=DB_DATE):
  """ return list of keywords of *cluster* at *date* 
      *all* is True it return list of keywords b/w *start*, *end* """

  try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not all: return cur.execute('SELECT c' +str(cluster)+ ' FROM keywords WHERE date_p=?', (date,)).fetchone()[0]
    else: return [row[0] for row in cur.execute('SELECT c' +str(cluster)+ ' FROM keywords WHERE date_p between ? and ?', (start, end)).fetchall()]

  except sqlite3.Error as error:
    print('error fetching data from keywords', error)


def rank_by_cluster(cluster, date=DB_DATE, all=False, start=DB_FIRST_DATE, end=DB_DATE):
  """ return list of rank sum  of *cluster* at *date* 
      *all* is True it return list of rank  b/w *start*, *end* """

  try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not all: return cur.execute('SELECT c' +str(cluster)+ ' FROM rank WHERE date_p=?', (date,)).fetchone()[0]
    else: return [row[0] for row in cur.execute('SELECT c' +str(cluster)+ ' FROM rank WHERE date_p between ? and ?', (start, end)).fetchall()]

  except sqlite3.Error as error:
    print('error fetching data from rank', error)


def size_by_cluster(cluster, date=DB_DATE, all=False, start=DB_FIRST_DATE, end=DB_DATE):
  """ return list of size  of *cluster* at *date* 
      *all* is True it return list of size  b/w *start*, *end* """

  try:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    if not all: return cur.execute('SELECT c' +str(cluster)+ ' FROM size WHERE date_p=?', (date,)).fetchone()[0]
    else: return [row[0] for row in cur.execute('SELECT c' +str(cluster)+ ' FROM size WHERE date_p between ? and ?', (start, end)).fetchall()]

  except sqlite3.Error as error:
    print('error fetching data from size', error)


def cluster_all_info(cluster, date=DB_DATE, all=False, start=DB_FIRST_DATE, end=DB_DATE):
  """ return dictionary with keys ('rank', 'size', 'keywords') of cluster at *date*
      *all* is True it return all_info b/w *start*, *end* """

  try:
    rank = rank_by_cluster(cluster, date, all, start, end)
    size = size_by_cluster(cluster, date, all, start, end)
    keywords = keywords_by_cluster(cluster, date, all, start, end)
    return {'rank': rank, 'size': size, 'keywords': keywords}
  except:
    print('error fetching all info of cluster', cluster)


def get_all_info(clusters=None, date=DB_DATE, all=True, start=DB_FIRST_DATE, end=DB_DATE):
  """ params-: list of clusters, in case of None it return info of all clusters 
      return -: dictionary with key cluster map with dict {rank', 'size', 'keywords'} of cluster in *clusters* at *date*
      if *all* is True it return all_info b/w *start*, *end* """
  
  try:
    if clusters is None: clusters = [i for i in range(MAX_CLUSTER)]
    res = {}
    for i in clusters:
      res[i] = cluster_all_info(i, date, all, start, end)
    return res
  except Exception as e:
    print('Error in get_all_info', e)
    return {}


def cluster_info_bw_date(cluster=0, start=DB_FIRST_DATE, end=DB_DATE):
  """ return list of dictionary with fields ('date', keywords, rank, size) 
      Note it assume 0 based indexing of cluster """

  str_to_date = lambda s: date(int(s[0:4]),int(s[5:7]),int(s[8:10]))
  start = str_to_date(start)
  end = str_to_date(end)

  try:
    res = []
    while(start <= end):
      data = cluster_all_info(cluster, start)
      rank = DB_DEFAULT_RANK
      if data['size'] > 0: rank =  data['rank'] // data['size'] 
      res.append({'rank':rank, 'keywords':data['keywords'], 'size': data['size'], 'date':str(start)})
      start += timedelta(days=1)
    return res
  except Exception as e:
    print('error in cluster_info_bw_date', e)
    return []
  
def allClusterData(endDate,tableName):
    """ return list of objects of 100 clusters which consist of rank,rank change with respect to previous 
    day information i.e  {date,cluster_no,cluster_name,rank,rankchange}"""
  try:
    str_to_date = lambda s: date(int(s[0:4]),int(s[5:7]),int(s[8:10]))
    strDate=str(str_to_date(endDate)-timedelta(days=1))
    if(strDate<DB_FIRST_DATE or endDate>DB_DATE): return [] 
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * from "+str(tableName)+" where date_p between ? and ?",(strDate,endDate))
    rows=cur.fetchall()
    dataList=[]
    for i in range(1,101):
      dataList.append({'date':endDate,'cluster_no':i,'cluster_name':i,'primary':rows[1][i],'secondary':rows[1][i]-rows[0][i]})
    return dataList  
  except Exception as e:
    print('error fetching data from rank table', e)
    return []
