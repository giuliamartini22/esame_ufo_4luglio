from database.DB_connect import DBConnect
from model.edge import Edge
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings(anno, stato):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from sighting s, state st
                        where s.state = st.id 
                        and Year(s.`datetime`) = %s
                        and st.Name  = %s """
            cursor.execute(query, (anno, stato))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct Year(s.`datetime`) as year
                        from sighting s, state st
                        where s.state = st.id 
                        order by Year(s.`datetime`) asc """
            cursor.execute(query)

            for row in cursor:
                result.append(row["year"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_states(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.Name as name
                        from sighting s, state st
                        where s.state = st.id 
                        and Year(s.`datetime`) = %s
                        order by st.Name asc """
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["name"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllEdges(anno, stato):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select s1.id as id1, s1.latitude as Lat1, s1.longitude as Lon1, s2.id as id2,  s2.latitude as Lat2, s2.longitude as Lon2
                        from sighting s1, sighting s2, state st1, state st2
                        where year(s1.`datetime`) = %s
                        and year(s2.`datetime`) = %s
                        and s1.shape = s2.shape
                        and st1.Name = %s
                        and st2.Name = %s
                        and s2.state = st2.id and s1.state = st1.id 
                        and s1.id <> s2.id """

        cursor.execute(query, (anno, anno, stato, stato,))

        for row in cursor:
            result.append((row["id1"], row["Lat1"], row["Lon1"], row["id2"], row["Lat2"], row["Lon2"]))

        cursor.close()
        conn.close()
        return result