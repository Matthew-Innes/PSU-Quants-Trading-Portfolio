import mysql.connector as mysql

def get_connection():
    return mysql.connect(
        host = "psu-quants.c3obwjkblypq.us-east-2.rds.amazonaws.com",
        user = "root",
        passwd = "jerpxl-dd8zQm-ussply",
        database = "tradedb"
    )
    
if __name__ == "__main__":
    mydb = get_connection()
    mycursor = mydb.cursor()