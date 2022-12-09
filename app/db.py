import sqlite3

class Database:
    def __init__(self) -> None:
        self.connect = self.dbcon()
        self.connect.row_factory = sqlite3.Row
        self.cursor = self.connect.cursor()

    def getAllSensors(self) -> dict:
        self.cursor.execute("SELECT id, description, qty FROM Sensors")
        self.connect.commit()
        return self.fetchAll(self.cursor.fetchall())

    def getSensorById(self, item_id) -> dict:
        self.cursor.execute("SELECT id, description, qty FROM Sensors WHERE id = :id", {"id": item_id})
        self.connect.commit()
        return self.fetchOne(self.cursor.fetchone())

    def createSensor(self, desc, qty) -> bool:
        self.cursor.execute('INSERT INTO Sensors (description, qty) VALUES (:desc, :qty)', {"desc": desc, "qty": qty})
        self.connect.commit()
        return True

    def updateSensor(self, item_id, desc, qty) -> bool:
        if self.getSensorById(item_id) == {}:
            return False
        self.cursor.execute('UPDATE Sensors SET description = :desc, qty = :qty WHERE id = :id',
                            {"desc":desc, "qty":qty, "id":item_id}
                            )
        self.clearParamsBySensorId(item_id)
        self.connect.commit()
        return True

    def deleteSensorById(self, item_id) -> bool:
        if self.getSensorById(item_id) == {}:
            return False
        self.cursor.execute('DELETE FROM Sensors WHERE id = :id', {"id": item_id})
        self.connect.commit()
        self.deleteSensorParamsById(id)
        return True

    def deleteSensorParamsById(self, item_id) -> bool:
        self.cursor.execute('DELETE FROM sensorinfo WHERE sensor_id = :sensor_id', {"sensor_id": item_id})
        self.connect.commit()
        return True

    def getSensorInfoById(self, item_id) -> dict:
        self.cursor.execute("SELECT param FROM sensorinfo WHERE sensor_id = :sensor_id", {"sensor_id": item_id})
        self.connect.commit()
        return self.fetchAll(self.cursor.fetchall())

    def createParamSensorInfo(self, item_id, value) -> bool:
        if self.getSensorById(item_id) == {}:
            return False
        self.cursor.execute('INSERT INTO sensorinfo (sensor_id, param) VALUES (:sensor_id, :param)', {"sensor_id":item_id, "param": value})
        self.connect.commit()
        self.clearParamsBySensorId(item_id)
        return True

    def clearParamsBySensorId(self, item_id):
        qty = self.countParamsBySensorId(item_id)
        maxQty = self.getSensorById(item_id)['qty']
        if (maxQty < qty):
            self.cursor.execute("DELETE FROM sensorinfo WHERE id in (SELECT id FROM sensorinfo WHERE sensor_id = :id ORDER BY id LIMIT :qty)",
                                {"id":item_id, "qty": qty-maxQty}
                                )
            self.connect.commit()
            return True

    def fetchAll(self, cursor):
        if cursor == None:
            return []
        result = [];
        for row in cursor:
            result.append(dict(row));
        return result

    def fetchOne(self, cursor):
        if cursor == None:
            return {}
        return dict(cursor)

    def countParamsBySensorId(self, item_id):
        self.cursor.execute("SELECT count(*) as cnt FROM sensorinfo WHERE sensor_id = :sensor_id", {"sensor_id": item_id})
        self.connect.commit()
        return dict(self.cursor.fetchone())['cnt']

    def dbcon(self):
        return sqlite3.connect('./sensors.db', check_same_thread=False)