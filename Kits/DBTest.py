from MSSQL import *



def main():
    ms = MSSQL(host="localhost",user="sa",pwd="sa",db="Oats")
    resList = ms.ExecQuery("select StockCode,StockName from M_StockInfo")
    for (StockCode,StockName) in resList:
        print StockName

if __name__ == '__main__':
    main()
