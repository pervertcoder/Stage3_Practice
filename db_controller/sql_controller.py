from db_controller.pool import get_db_connect

# 留言資料寫入
def write_message(cont:str):
    conn = get_db_connect()
    mycursor = conn.cursor()
    mycursor.execute("use message_photo;")
    sql = "insert into message(content)values(%s)"
    mycursor.execute(sql, (cont,))

    conn.commit()
    conn.close()
    print("data insert successfully")
# 留言資料取得
def get_message():
    conn = get_db_connect()
    mycursor = conn.cursor()
    mycursor.execute("use message_photo;")
    sql = "select * from message"
    mycursor.execute(sql)

    result = [x[1] for x in mycursor]
    conn.close()
    return result
# 刪除所有資料
def delete():
    conn = get_db_connect()
    mycursor = conn.cursor()
    mycursor.execute("use message_photo;")
    sql = "truncate table message;"
    mycursor.execute(sql)

    conn.commit()
    conn.close()
    print("data deleted successfully")