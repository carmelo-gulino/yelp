from database.DB_connect import DBConnect
from model.business import Business
from model.review import Review


class DAO:
    def __init__(self):
        pass

    @staticmethod
    def get_all_cities():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select distinct b.city from business b order by b.city """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row['city'])
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_locali(city):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from business b where b.city = %s order by b.business_name"""
        cursor.execute(query, (city,))
        result = []
        for row in cursor:
            result.append(Business(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_reviews(business_id):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from reviews r where r.business_id = %s"""
        cursor.execute(query, (business_id,))
        result = []
        for row in cursor:
            result.append(Review(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_weighted_edges(review_date, reviews_map):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select r.review_id , r.review_date
                    from reviews r 
                    where r.review_date > %s
                    group by r.review_id """
        cursor.execute(query, (review_date,))
        result = []
        for row in cursor:
            if row['review_id'] in reviews_map:
                result.append((reviews_map[row['review_id']], row['review_date']))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_reviews():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """select * from reviews"""
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Review(**row))
        cursor.close()
        cnx.close()
        return result