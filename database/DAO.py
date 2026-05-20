from database.DB_connect import DBConnect
from model.artist import Artista


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

    @staticmethod

    def getAllNodes(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct ar.ArtistId , ar.Name
                    from artist ar 
                    join album al on ar.ArtistId = al.ArtistId 
                    join track t on al.AlbumId = t.AlbumId 
                    join genre g on t.GenreId = g.GenreId 
                    where g.name = ? """

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()

        return result

