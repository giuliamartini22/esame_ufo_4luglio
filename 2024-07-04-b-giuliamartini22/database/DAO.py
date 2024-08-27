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
    def get_all_edges():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.id as s1,  s2.id as s2
                        from sighting s, sighting s2
                        where s2.shape = s.shape
                        and s2.id != s.id
                                            """
            cursor.execute(query)

            for row in cursor:
                result.append(Edge(**row))
            cursor.close()
            cnx.close()
        return result