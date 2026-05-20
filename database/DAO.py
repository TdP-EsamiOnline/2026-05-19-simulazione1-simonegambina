from database.DB_connect import DBConnect
from model.artist import Artista


class DAO():

    @staticmethod
    def getAllGenre():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select g.name
                from genre g
                order by g.name"""

        cursor.execute(query)

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllNodes(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT ar.ArtistId, ar.Name
            FROM artist ar 
            JOIN album al ON ar.ArtistId = al.ArtistId 
            JOIN track t ON al.AlbumId = t.AlbumId 
            JOIN genre g ON t.GenreId = g.GenreId 
            WHERE g.Name = %s
        """

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(Artista(**row))

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getAllEdges(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """
            SELECT DISTINCT 
                ca1.ArtistId AS idArtista1,
                ca2.ArtistId AS idArtista2,
                p1.popolarita AS popolarita1,
                p2.popolarita AS popolarita2,
                p1.popolarita + p2.popolarita AS peso
            FROM (
                SELECT DISTINCT i.CustomerId, ar.ArtistId
                FROM invoice i
                JOIN invoiceline il ON i.InvoiceId = il.InvoiceId
                JOIN track t ON il.TrackId = t.TrackId
                JOIN album al ON t.AlbumId = al.AlbumId
                JOIN artist ar ON al.ArtistId = ar.ArtistId
                JOIN genre g ON t.GenreId = g.GenreId
                WHERE g.Name = %s
            ) ca1
            JOIN (
                SELECT DISTINCT i.CustomerId, ar.ArtistId
                FROM invoice i
                JOIN invoiceline il ON i.InvoiceId = il.InvoiceId
                JOIN track t ON il.TrackId = t.TrackId
                JOIN album al ON t.AlbumId = al.AlbumId
                JOIN artist ar ON al.ArtistId = ar.ArtistId
                JOIN genre g ON t.GenreId = g.GenreId
                WHERE g.Name = %s
            ) ca2
                ON ca1.CustomerId = ca2.CustomerId
                AND ca1.ArtistId < ca2.ArtistId
            JOIN (
                SELECT ar.ArtistId, SUM(il.Quantity) AS popolarita
                FROM artist ar
                JOIN album al ON ar.ArtistId = al.ArtistId
                JOIN track t ON al.AlbumId = t.AlbumId
                JOIN genre g ON t.GenreId = g.GenreId
                JOIN invoiceline il ON t.TrackId = il.TrackId
                JOIN invoice i ON il.InvoiceId = i.InvoiceId
                WHERE g.Name = %s
                GROUP BY ar.ArtistId
            ) p1 ON ca1.ArtistId = p1.ArtistId
            JOIN (
                SELECT ar.ArtistId, SUM(il.Quantity) AS popolarita
                FROM artist ar
                JOIN album al ON ar.ArtistId = al.ArtistId
                JOIN track t ON al.AlbumId = t.AlbumId
                JOIN genre g ON t.GenreId = g.GenreId
                JOIN invoiceline il ON t.TrackId = il.TrackId
                JOIN invoice i ON il.InvoiceId = i.InvoiceId
                WHERE g.Name = %s
                GROUP BY ar.ArtistId
            ) p2 ON ca2.ArtistId = p2.ArtistId
        """

        cursor.execute(query, (genere, genere, genere, genere))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

    @staticmethod
    def getArtistGenre(genere):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.name, ar.Name 
                    from Genre g 
                    join Track t on g.GenreId = t.GenreId 
                    join album al on t.AlbumId = al.AlbumId 
                    join Artist ar on al.ArtistId  = ar.ArtistId 
                    where g.name = %s 
                    order by ar.Name"""

        cursor.execute(query, (genere,))

        for row in cursor:
            result.append(row)

        cursor.close()
        conn.close()

        return result

