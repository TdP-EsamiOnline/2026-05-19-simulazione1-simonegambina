from database.DB_connect import DBConnect


class DAO():

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.name
                from genre g"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["name"])

        cursor.close()
        conn.close()

        return result
