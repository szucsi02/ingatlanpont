from models import HirdetesModel
import pymysql
class HirdetesController:

    def hirdetes_kereses(self, search_term, location, connection):
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

    def hirdetes_szures(self, szures=None, connection=None):
        if szures is None:
            szures = ['', '', '', '']
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
        else:
            return results

        return results

    def hirdetes_hozzaad(self, hirdetes: 'HirdetesModel') -> None:
        pass
    def hirdetes_modosit(self, hirdetes_id: int) -> None:
        pass
    def hirdetes_torles(self, hirdetes_id: int) -> None:
        pass



    def get_hirdetes_by_id(self, hirdetes_id, db_config):
        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM Hirdetes WHERE id = %s"
                cursor.execute(sql, (hirdetes_id,))
                hirdetes = cursor.fetchone()
            return hirdetes
        finally:
            connection.close()

