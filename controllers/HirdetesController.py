from models import HirdetesModel
import pymysql
class HirdetesController:

    def hirdetes_kereses(self, search_term, location, connection):
        cursor = connection.cursor()
        try:
            with connection.cursor() as cursor:
                if search_term and location:
                    sql = "SELECT * FROM Hirdetes WHERE telek LIKE %s AND cim LIKE %s"
                    cursor.execute(sql, ('%' + search_term + '%', '%' + location + '%'))
                elif search_term:
                    sql = "SELECT * FROM Hirdetes WHERE telek LIKE %s"
                    cursor.execute(sql, ('%' + search_term + '%',))
                elif location:
                    sql = "SELECT * FROM Hirdetes WHERE cim LIKE %s"
                    cursor.execute(sql, ('%' + location + '%',))
                else:
                    sql = "SELECT * FROM Hirdetes"
                    cursor.execute(sql)
                results = cursor.fetchall()
        finally:
            connection.close()
        return results

    def hirdetes_szures(self, szures, connection):
        rooms, area, search_query, location = szures
        results = self.hirdetes_kereses(search_query, location, connection)

        if rooms:
            try:
                rooms = int(rooms)
                results = [r for r in results if r['szobakSzama'] >= rooms]
            except ValueError:
                pass  # Ignore if rooms is not a valid integer
        if area:
            results = [r for r in results if r['alapterulet'] >= int(area)]

        return results

    def hirdetes_hozzaad(self, hirdetes: 'HirdetesModel') -> None:
        pass
    def hirdetes_modosit(self, hirdetes_id: int) -> None:
        pass
    def hirdetes_torles(self, hirdetes_id: int) -> None:
        pass