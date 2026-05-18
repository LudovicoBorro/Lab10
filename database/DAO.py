from database.DB_connect import DBConnect
from model.country import Country
from model.contiguity import LandContiguity

class DAO:
    def __init__(self):
        pass

    @staticmethod
    def getAllCountry():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """
                select *
                from country c
        """

        cursor.execute(query)

        for row in cursor:
            res.append(Country(**row))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllNodes(year: int, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """
                select c.state1no
                from contiguity c 
                where c.year <= %s
        """

        cursor.execute(query, (year,))

        for row in cursor:
            res.append(idMap.get(row["state1no"]))

        cursor.close()
        conn.close()
        return res

    @staticmethod
    def getAllEdges(year: int, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)

        res = []

        query = """
                select c.state1no, c.state2no, year
                from contiguity c 
                where c.conttype = 1 and c.year <= %s
        """

        cursor.execute(query, (year,))

        for row in cursor:
            res.append(LandContiguity(idMap.get(row["state1no"]), idMap.get(row["state2no"]), row["year"]))

        cursor.close()
        conn.close()
        return res