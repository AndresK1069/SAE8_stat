import oracledb

with oracledb.connect(user="kpognon", password="azerty",host="192.168.24.52",port="1521",service_name="FREEPDB1") as connection:
    with connection.cursor() as cursor:


        sql = """
        SELECT NO2, HORAIRE 
        FROM V_MESURES_FRANCE 
        WHERE EXTRACT(MONTH FROM HORAIRE) IN (7, 12)
        """

        for row in cursor.execute(sql):
            print(row)
