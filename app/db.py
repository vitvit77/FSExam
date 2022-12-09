import sqlite3

class Database:
    def __init__(self) -> None:
        self.connect = sqlite3.connect('./sensors.db')
        self.cursor = self.connect.cursor()

    def getAllSensors(self) -> list:
        self.cursor.execute("SELECT id, description, qty FROM Sensors")
        return self.cursor.fetchall()

    def getSensorById(self, id) -> dict:
        self.cursor.execute("SELECT id, description, qty FROM Sensors WHERE id = :id", {"id": id})
        return self.cursor.fetchone()

    def createSensor(self, desc, qty) -> bool:
        self.cursor.execute('INSERT INTO Sensors (description, qty) VALUES (:desc, :qty)', {"desc": desc, "qty": qty})
        self.connect.commit()
        return True

    def updateSensor(self, id, desc, qty) -> bool:
        if self.getSensorById(id) == None:
            return False
        self.cursor.execute('UPDATE Sensors SET description = :desc, qty = :qty WHERE id = :id', {"desc":desc, "qty":qty, "id":id})
        self.clearParamsBySensorId(id)
        self.connect.commit()
        return True

    def deleteSensorById(self, id) -> bool:
        self.cursor.execute('DELETE FROM Sensors WHERE id = :id', {"id": id})
        self.connect.commit()
        self.deleteSensorParamsById(id)
        return True

    def deleteSensorParamsById(self, id) -> bool:
        self.cursor.execute('DELETE FROM sensorinfo WHERE sensor_id = :sensor_id', {"sensor_id": id})
        self.connect.commit()
        return True

    def getSensorInfoById(self, id) -> dict:
        self.cursor.execute("SELECT param FROM sensorinfo WHERE sensor_id = :sensor_id", {"sensor_id": id})
        return self.cursor.fetchall()

    def createParamSensorInfo(self, item_id, value) -> bool:
        if self.getSensorById(item_id) == None:
            return False
        self.cursor.execute('INSERT INTO sensorinfo (sensor_id, param) VALUES (:sensor_id, :param)', {"sensor_id":item_id, "param": value})
        self.connect.commit()
        self.clearParamsBySensorId(item_id)
        return True

    def clearParamsBySensorId(self, id):
        qty = self.countParamsBySensorId(id)
        maxQty = self.getSensorById(id)['qty']
        if (maxQty < qty):
            self.cursor.execute("DELETE FROM sensorinfo WHERE id in (select id from (SELECT id FROM sensorinfo WHERE sensor_id = %s ORDER BY id) as ttt) LIMIT %s", (id, qty-maxQty))
            self.connect.commit()
            return True

    def countParamsBySensorId(self, id):
        self.cursor.execute("SELECT count(*) as cnt FROM sensorinfo WHERE sensor_id = :sensor_id", {"sensor_id": id})
        return self.cursor.fetchone()['cnt']
