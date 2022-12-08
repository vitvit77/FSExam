import pymysql.cursors
from config import CONFIG

# Подключиться к базе данных. Открыл временно для всех IP. После сдачи / не сдачи уберу ))

class Database:
    def __init__(self) -> None:
        self.mydb = pymysql.connect(host=CONFIG['HOST'],
                               user=CONFIG['USER'],
                               password=CONFIG['PASS'],
                               db=CONFIG['DB'],
                               charset='utf8',
                               cursorclass=pymysql.cursors.DictCursor)

    def getAllSensors(self) -> list:
        with self.mydb.cursor() as cursor:
            cursor.execute("SELECT id, description, qty FROM Sensors")
            return cursor.fetchall()

    def getSensorById(self, id) -> dict:
        with self.mydb.cursor() as cursor:
            cursor.execute("SELECT id, description, qty FROM Sensors WHERE id = %s", (id))
            return cursor.fetchone()

    def createSensor(self, desc, qty) -> bool:
        with self.mydb.cursor() as cursor:
            cursor.execute('INSERT INTO Sensors (description, qty) VALUES (%s, %s)', (desc, qty))
            self.mydb.commit()
            return self.getLastInsertId()

    def updateSensor(self, id, desc, qty) -> bool:
        if self.getSensorById(id) == None:
            return False
        with self.mydb.cursor() as cursor:
            cursor.execute('UPDATE Sensors SET description = %s, qty = %s WHERE id = %s', (desc, qty, id))
            self.mydb.commit()
            self.clearParamsBySensorId(id)
            return True

    def deleteSensorById(self, id) -> bool:
        with self.mydb.cursor() as cursor:
            cursor.execute('DELETE FROM Sensors WHERE id = %s', (id))
            self.mydb.commit()
            self.deleteSensorParamsById(id)
            return True

    def deleteSensorParamsById(self, id) -> bool:
        with self.mydb.cursor() as cursor:
            cursor.execute('DELETE FROM sensorinfo WHERE sensor_id = %s', (id))
            self.mydb.commit()
            return True

    def getSensorInfoById(self, id) -> dict:
        with self.mydb.cursor() as cursor:
            cursor.execute("SELECT param FROM sensorinfo WHERE sensor_id = %s", (id))
            return cursor.fetchall()

    def createParamSensorInfo(self, item_id, value) -> bool:
        if self.getSensorById(item_id) == None:
            return False
        with self.mydb.cursor() as cursor:
            cursor.execute('INSERT INTO sensorinfo (sensor_id, param) VALUES (%s, %s)', (item_id, value))
            self.mydb.commit()
            self.clearParamsBySensorId(item_id)
            return True

    def clearParamsBySensorId(self, id):
        with self.mydb.cursor() as cursor:
            qty = self.countParamsBySensorId(id)
            maxQty = self.getSensorById(id)['qty']
            if (maxQty < qty):
                cursor.execute("DELETE FROM sensorinfo WHERE id in (select id from (SELECT id FROM sensorinfo WHERE sensor_id = %s ORDER BY id) as ttt) LIMIT %s", (id, qty-maxQty))
                self.mydb.commit()
                return True

    def countParamsBySensorId(self, id):
        with self.mydb.cursor() as cursor:
            cursor.execute("SELECT count(*) as cnt FROM sensorinfo WHERE sensor_id = %s", (id))
            return cursor.fetchone()['cnt']

    def getLastInsertId(self):
        with self.mydb.cursor() as cursor:
            cursor.execute("SELECT LAST_INSERT_ID() as id")
            return cursor.fetchone()['id']