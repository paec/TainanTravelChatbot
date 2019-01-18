import pymysql




def querydb(para,conn,cursor):


    result = ""

    try:
        cursor.execute(para)
        result = cursor.fetchall()

        
    except Exception as e:
        conn.rollback()
        print(e)

    finally:

        # cursor.close()
        # conn.close()
        return result


if __name__ == '__main__':


    result = querydb("SELECT entity FROM `BookingChatbot_Entity` WHERE name = '飯店'")

    print(result)