import oracledb

with oracledb.connect(user="kpognon", password="azerty",host="192.168.24.52",port="1521",service_name="FREEPDB1") as connection:
    with connection.cursor() as cursor:


        sql = """
            SELECT * FROM MESURE_PEKIN_STATION1002   
            WHERE (TRUNC(HORAIRE), STATION_ID) = (
            SELECT TRUNC(HORAIRE), STATION_ID
            FROM MESURE_PEKIN_STATION1002  
            WHERE NO2 = (SELECT MAX(NO2) FROM MESURE_PEKIN_STATION1002)
            FETCH FIRST 1 ROW ONLY)
            ORDER BY HORAIRE
        """

        for row in cursor.execute(sql):
            print(row)
