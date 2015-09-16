from MSSQL import *
import pyodbc

SQLSERVERLOCAL='Driver={SQL Server Native Client 11.0};Server=(localdb)\v11.0;integrated security = true;DATABASE=Oats;'

def main():
    #ms = MSSQL(host="(localdb)\v11.0",user="sa",pwd="123456",db="Oats")
    #conn = pyodbc.connect('DRIVER={SQL Server};SERVER=(localdb)\v11.0;DATABASE=Oats;integrated security = true')
    conn = pyodbc.connect(SQLSERVERLOCAL)
    cursor=conn.cursor()
    cursor.execute("SELECT StockCode,StockName FROM M_StockInfo")
    rows = cursor.fetchall()

    for row in rows:
        print row.StockCode, row.StockName

if __name__ == '__main__':
    main()
