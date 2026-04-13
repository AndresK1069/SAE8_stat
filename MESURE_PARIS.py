import oracledb

with oracledb.connect(user="kpognon", password="azerty",host="192.168.24.52",port="1521",service_name="FREEPDB1") as connection:
    with connection.cursor() as cur:


        sql = """
            SELECT * FROM MESURE_PARIS_PROPRE   
            WHERE (TRUNC(HORAIRE), STATION_ID) = (
            SELECT TRUNC(HORAIRE), STATION_ID
            FROM MESURE_PARIS_PROPRE  
            WHERE NO2 = (SELECT MAX(NO2) FROM MESURE_PARIS_PROPRE)
            FETCH FIRST 1 ROW ONLY)
            ORDER BY HORAIRE
        """

        for row in cursor.execute(sql):
            print(row)
#Le script pour la presentation


import oracledb
import matplotlib.pyplot as plt

def generate_full_stats_png(cursor, select_cols, group_cols, title, filename, headers):
    sql = f"""
    SELECT 
        {select_cols}, 
        MIN(NO2), MAX(NO2), MAX(NO2)-MIN(NO2), ROUND(AVG(NO2),2), ROUND(VARIANCE(NO2),2),
        ROUND(PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY NO2),2),
        ROUND(MEDIAN(NO2),2),
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY NO2),2),
        ROUND(PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY NO2) - PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY NO2), 2)
    FROM MESURE_SHANGHAI_STATION2001
    WHERE NO2 IS NOT NULL
    GROUP BY {group_cols} 
    ORDER BY {group_cols}"""
    
    cursor.execute(sql)
    data = cursor.fetchall()

    if data:
        fig, ax = plt.subplots(figsize=(18, len(data) * 0.5 + 2))
        ax.axis('off')
        tab = ax.table(cellText=data, colLabels=headers, loc='center', cellLoc='center')
        tab.auto_set_font_size(False)
        tab.set_fontsize(8)
        tab.scale(1, 2) 
        
        plt.title(title, fontweight='bold', fontsize=15, pad=30)
        #plt.savefig(os.path.join(output_dir, filename), bbox_inches='tight', dpi=150)
        plt.close()
        print(f"Généré : {filename}")

try:
    with oracledb.connect(user="kpognon", password="azerty",host="192.168.24.52",port="1521",service_name="FREEPDB1") as connection:
        with connection.cursor() as cursor:
            # 1. PAR STATION (GLOBAL)
            h_stat = ["STATION", "MIN", "MAX", "ETEND.", "MOY", "VAR", "Q1", "MED", "Q3", "IQR"]
            generate_full_stats_png(cur, "STATION_ID", "STATION_ID", 
                                   "Stats Globales par Station", "stats_station.png", h_stat)
            
            # 2. PAR STATION ET PAR MOIS (LIGNES MISES À JOUR)
            h_mois = ["STATION", "MOIS", "MIN", "MAX", "ETEND.", "MOY", "VAR", "Q1", "MED", "Q3", "IQR"]
            generate_full_stats_png(cur, "STATION_ID, TO_CHAR(HORAIRE, 'YYYY-MM')", 
                                   "STATION_ID, TO_CHAR(HORAIRE, 'YYYY-MM')", 
                                   "Stats par Station et par Mois", "stats_mois.png", h_mois)
except Exception as e:
    print(f"Erreur : {e}")
