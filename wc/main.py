import mysql.connector
import requests
from bs4 import BeautifulSoup
import re
import csv


# define crawler 
def crawler(stock,columns_list):
    """
    Parameters:
    stock = name of the stock in string, eg. "AAPL"
    columns_list = the list of columns of the data with the keyword,
        eg. [['Price', 'span', 'TextLabel__text-label___3oCVw TextLabel__black___2FN-Z TextLabel__light___1WILL digits last QuoteRibbon-digits-30Sds']]

    Return:
    data_dict = a dictionary of the data for the stock, eg. {'Price': '135.36'}
    """
    data_dict = {}
    try:
        #get html
        datas = requests.get(f"https://www.reuters.com/companies/{stock}.N/key-metrics")
        soup = BeautifulSoup(datas.content, 'lxml')
        #get data for each column
        for column in columns_list:
            raw = soup.find(column[2], {'class': column[3]})
            data = re.findall(re.compile(r'>([\s\S]+?)<'), str(raw))[0]
            if column[1]== 'num':
                data = float(data.replace(',',''))
            data_dict[column[0]]=data
    except Exception as e:
        print(f"Crawling {stock} failed.",e)

    return data_dict
 
# define function to insert data to database
def insert_stock(stock,data_dict,mycursor):
    """
    Parameters:
    stock = name of the stock in string, eg. "AAPL"
    data_dict = a dictionary of the data for the stock, eg. {'Price': '135.36'}
    mycursor = the cursor for the database,
        eg. mysql.connector.connect(
          host="localhost",
          user="root",
          database="stock_analysis"
        ).cursor()

    This function insert the data to database
    """
    try:
        keys = ""
        vals = ""
        for data in data_dict.items():
            keys += data[0]+", "
            vals += f"'{data[1]}', "

        sql = f"INSERT INTO newtable (Stock, {keys}Updated) VALUES ('{stock}', {vals}CURRENT_TIME)"
        mycursor.execute(sql)
    except Exception as e:
        print(f"Inserting {stock} failed.",e)


# start running
if __name__ == "__main__":

    # list of stocks to be checked
    stocks_list=[]
    with open('stocks_list.csv', newline='') as csvfile:
         stocks = csv.reader(csvfile)
         for stock in stocks:
             stocks_list.append(stock[0])


    # list of columns to be checked
    columns_list=[]
    with open('columns.csv', newline='') as csvfile:
         columns = csv.reader(csvfile)
         for column in columns:
             columns_list.append(column)



    # connect to database
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      #password="yourpassword",
      database="stock_analysis"
    )
    mycursor = mydb.cursor()

    for stock in stocks_list:
        data_dict = crawler(stock,columns_list)
        insert_stock(stock,data_dict,mycursor)

    # commit the changes ans close the connection to database
    mydb.commit()
    mycursor.close()
    print("Done")
