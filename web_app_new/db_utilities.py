import sqlite3
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

from flask import current_app, g
from time import sleep

import click


# from . import client
from .device_utils import associate_device, client

from .device_utils import disconnect_device

DATABASE_NAME = "patient_data.db"
# DATABASE_PATH = os.path.join(current_app.instance_path, DATABASE_NAME)
DATABASE_PATH = "/home/mladen/Desktop/TUES_FEST_2025/web_app_new/instance/" + DATABASE_NAME

@click.command('init-db')
def create_new_db():
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()
        print("Database was successfully created!")
        cur.execute("PRAGMA foreign_keys = ON;")

        # PatientDetails table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS PatientDetails (
                patientID INTEGER PRIMARY KEY,
                name TEXT,
                description TEXT,
                room_num INTEGER,
                pinned BOOLEAN
            );
        ''')

        # NodeID_to_PatientID table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS NodeID_to_PatientID (
                nodeID TEXT NOT NULL,
                patientID INTEGER NOT NULL,
                PRIMARY KEY (nodeID, patientID),
                FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
            );
        ''')

        # Notifications table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Notifications (
                notificationID INTEGER PRIMARY KEY,
                patientID INTEGER NOT NULL,
                type TEXT CHECK(type IN ('emergency','ordinary')),
                confirmed BOOLEAN,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
            );
        ''')

        # Notes table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS Notes (
                noteID INTEGER PRIMARY KEY,
                patientID INTEGER NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
            );
        ''')

        # UserData table
        cur.execute('''
            CREATE TABLE IF NOT EXISTS UserData (
                userID INTEGER PRIMARY KEY,
                name TEXT,
                speciality TEXT,
                username TEXT,
                password TEXT
            );
        ''')

        con.commit()

class PatientDB:
    def __init__(self):
        if not os.path.isfile(DATABASE_PATH):
            create_new_db()
        self.client = InfluxDBClient(
            url='http://localhost:8086',
            token='r2xnS1k57vPE_i1mgpINBHIwIuTb_ELtzDn8NHrV9hbXFY0ge_PRD3cTQFu7TyC3EG2K4XKfP8NKPd1R-9LtJw==',
            org='Robo'
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()

    

    
    

   

    

    # ----- Notification & Note -----
    
    # def remove_note(self, noteID):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         con.cursor().execute("DELETE FROM Notes WHERE noteID = ?", (noteID,)); con.commit()

    # ----- Patient edits -----
   

    # ----- Notification & Note edits -----
    # def edit_notification(self, notificationID, n_type=None, confirmed=None, timestamp=None):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         updates, params = [], []
    #         if n_type: updates.append("type = ?"); params.append(n_type)
    #         if confirmed is not None: updates.append("confirmed = ?"); params.append(confirmed)
    #         if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
    #         params.append(notificationID)
    #         con.cursor().execute(f"UPDATE Notifications SET {', '.join(updates)} WHERE notificationID = ?", params)
    #         con.commit()

    # def edit_note(self, noteID, description=None, timestamp=None):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         updates, params = [], []
    #         if description: updates.append("description = ?"); params.append(description)
    #         if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
    #         params.append(noteID)
    #         con.cursor().execute(f"UPDATE Notes SET {', '.join(updates)} WHERE noteID = ?", params)
    #         con.commit()

    # ----- Measurement inserts -----
    
    
    # ------ Measurment methods

    def add_temperature(self, patientID, temperature):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            point = Point("temp").tag("PatientID", patientID).field("temp", temperature)
            self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
            print(f"Temperature {temperature} added for PatientID {patientID}.")
            return True
        else:
            return None
    
    def add_bpm(self, patientID, bpm):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            point = Point("bpm").tag("PatientID", patientID).field("bpm", bpm)
            self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
            print(f"BPM {bpm} added for PatientID {patientID}.")
            return True
        else:
            return None

    def get_latest_measurement_records(self, patientID, measurement, n):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            quzery = f'''
            from(bucket: "patient_measurements")
            |> range(start: -1h)
            |> filter(fn: (r) => r["_measurement"] == "{measurement}")
            |> filter(fn: (r) => r["PatientID"] == "{patientID}")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n: {n})
            '''

            '''
            from(bucket: "patient_measurements")
            |> range(start: v.timeRangeStart, stop: v.timeRangeStop)
            |> filter(fn: (r) => r["_measurement"] == "bpm")
            |> filter(fn: (r) => r["PatientID"] == "1")
            |> limit(n: 2) 

            '''
            result = self.query_api.query(org='Robo', query=quzery)
            records = []
            for table in result:
                for record in table.records:
                    records.append({
                        "time": record.get_time(),
                        "measurement": record.get_measurement(),
                        "field": record.get_field(),
                        "value": record.get_value()
                    })
            return records
        else:
            return None
    
    def delete_measurements_patient_records(self, patientID):
            patient = self.get_patient(patientID=patientID)
            if patient is not None:
                start = "1970-01-01T00:00:00Z"
                stop = datetime.utcnow().isoformat() + "Z"
                predicate = f'PatientID="{patientID}"'
                self.delete_api.delete(start, stop, predicate, bucket="patient_measurements", org='Robo')
                print(f"All records for PatientID {patientID} have been deleted.")
                return True
            else:
                return None

    # from datetime import datetime

   
    # def delete_measurements_patient_records(self, patientID):
    #     """
    #     Delete all data points and drop series (including tag metadata) for 'temp' and 'bpm' measurements for the given PatientID.
    #     """
    #     # Verify that the patient exists in SQLite
    #     if not self.get_patient(patientID=patientID):
    #         return None

    #     measurements = ["temp", "bpm"]
    #     for measurement in measurements:
    #         # Construct a Flux script to drop the series for this measurement and PatientID
    #         flux = (
    #             f'import "influxdata/influxdb/schema',
    #             f'schema.dropSeries(bucket: "patient_measurements',
    #             f'predicate: (r) => r._measurement == "{measurement}" and r["PatientID"] == "{patientID}")'
    #         )
    #         # Execute the Flux script via the query API
    #         self.query_api.query(org='Robo', query=flux)

    #     print(f"All series and data for PatientID {patientID} have been dropped.")
    #     return True




    # # ----- Search patients by criteria -----
    # def search_patients(self, name=None, description=None, room_num=None, pinned=None, nodeID=None):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         query = "SELECT patientID, name, description, room_num, pinned FROM PatientDetails"
    #         conditions = []
    #         params = []
    #         if name is not None:
    #             conditions.append("name = ?")
    #             params.append(name)
    #         if description is not None:
    #             conditions.append("description = ?")
    #             params.append(description)
    #         if room_num is not None:
    #             conditions.append("room_num = ?")
    #             params.append(room_num)
    #         if pinned is not None:
    #             conditions.append("pinned = ?")
    #             params.append(pinned)
    #         if nodeID is not None:
    #             conditions.append("patientID IN (SELECT patientID FROM NodeID_to_PatientID WHERE nodeID = ?)")
    #             params.append(nodeID)
    #         if conditions:
    #             query += " WHERE " + " AND ".join(conditions)
    #         cur.execute(query, params)
    #         rows = cur.fetchall()
    #         return [dict(row) for row in rows]

    # ----- Fetch full patient details -----
    
    # ----- Search patients by criteria -----
    # def search_patients(self, name=None, description=None, room_num=None, pinned=None):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         query = "SELECT patientID, name, description, room_num, pinned FROM PatientDetails"
    #         conditions = []
    #         params = []
    #         if name is not None:
    #             conditions.append("name = ?")
    #             params.append(name)
    #         if description is not None:
    #             conditions.append("description = ?")
    #             params.append(description)
    #         if room_num is not None:
    #             conditions.append("room_num = ?")
    #             params.append(room_num)
    #         if pinned is not None:
    #             conditions.append("pinned = ?")
    #             params.append(pinned)
    #         if conditions:
    #             query += " WHERE " + " AND ".join(conditions)

    #         cur.execute(query, params)
    #         return [dict(row) for row in cur.fetchall()]
        
    # def search_note(self, patientID):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         query = f"SELECT * FROM Notes WHERE patientID = {patientID}"
    #         cur.execute(query)
    #         return [dict(row) for row in cur.fetchall()]
    # def search_notification(self, patientID):
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         con.row_factory = sqlite3.Row
    #         cur = con.cursor()
    #         query = f"SELECT * FROM Notifications WHERE patientID = {patientID}"
    #         cur.execute(query)
    #         return [dict(row) for row in cur.fetchall()]
    # ----- Notification methods

    def get_notifications(self, patientID=None, notificationID=None, type=None, year=None, month=None, day=None, hour=None, minute=None):
        conditions = []
        params = []
        if patientID is not None:
            patient = self.get_patient(patientID=patientID)
            if patient is not None:
                conditions.append('patientID = ?')
                params.append(patientID)
            else:
                return None
        if notificationID is not None:
            conditions.append('notificationID = ?')
            params.append(notificationID)
        if type is not None:
            conditions.append('type = ?')
            params.append(type)
        if year is not None:
            conditions.append('strftime("%Y", timestamp) = ?')
            params.append(str(year))
        if month is not None:
            conditions.append('strftime("%m", timestamp) = ?')
            params.append(str(month).zfill(2))
        if day is not None:
            conditions.append('strftime("%d", timestamp) = ?')
            params.append(str(day).zfill(2))
        if hour is not None:
            conditions.append('strftime("%H", timestamp) = ?')
            params.append(str(hour).zfill(2))
        if minute is not None:
            conditions.append('strftime("%M", timestamp) = ?')
            params.append(str(minute).zfill(2))
        query = "SELECT * FROM Notifications"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with sqlite3.connect(DATABASE_PATH) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()
            return [dict(row) for row in rows] if rows else None

    def remove_notification(self, notificationID=None,patientID=None):
        if patientID is not None:
            patient = self.get_patient(patientID = patientID)
            if patient is not None:
                with sqlite3.connect(DATABASE_PATH) as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM Notifications WHERE patientID = ?", (patientID,))
                    con.commit()
                    return True
            else:
                return None
        notification = self.get_notifications(notificationID=notificationID)
        if notification is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                con.cursor().execute("DELETE FROM Notifications WHERE notificationID = ?", (notificationID,)); con.commit()
                return True
        else:
            return None
    def add_notification(self, patientID, n_type, confirmed):
        patient = self.get_patient(patientID=patientID)
        if patient  is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'INSERT INTO Notifications(patientID, type, confirmed, timestamp) VALUES(?,?,?,CURRENT_TIMESTAMP)',
                    (patientID, n_type, confirmed)
                )
                con.commit()
                return True
        else:
            return None
    
    def confirm_notification(self,patientID):
        print("CONFIRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRMMMMMMMMMMMMMMMMMMM")
        patient = self.get_patient(patientID=patientID)
        if patient:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                # Find the latest notification for the patient
                cur.execute(
                    "SELECT notificationID FROM Notifications WHERE patientID = ? ORDER BY notificationID DESC LIMIT 1",
                    (patientID,)
                )
                row = cur.fetchone()
                if row:
                    notificationID = row[0]
                    # Update the confirmed status to True (or 1)
                    cur.execute(
                        "UPDATE Notifications SET confirmed = 1 WHERE notificationID = ?",
                        (notificationID,)
                    )
                    con.commit()
                    print(f"Notification {notificationID} confirmed.")
                else:
                    print("No notifications found for this patient.")
        
    # ----- Notes methods

    def add_note(self, patientID, description):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'INSERT INTO Notes(patientID, description, timestamp) VALUES(?,?,CURRENT_TIMESTAMP)',
                    (patientID, description)
                )
                con.commit()
                return True
        else:
            return None
    
    def get_notes(self,patientID=None,noteID=None):
        conditions = []
        params = []
        if patientID is not None:
            patient = self.get_patient(patientID=patientID)
            if patient is not None:
                conditions.append('patientID = ?')
                params.append(patientID)
            else:
                return None
        if noteID is not None:
            conditions.append('noteID = ?')
            params.append(noteID)
        
        query = "SELECT * FROM Notes"
        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Execute the query
        with sqlite3.connect(DATABASE_PATH) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(query, params)
            rows = cur.fetchall()

            # Return the results as a list of dictionaries
            return [dict(row) for row in rows] if rows else None



    def edit_note(self,noteID, description):
        note = self.get_notes(noteID=noteID)
        if note is not None:
             with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'UPDATE Notes SET description = ? WHERE noteID = ?',
                    (description, noteID)
                )
                con.commit()
                return True
        else:
            return None
    
    def remove_note(self,noteID=None,patientID=None):
        if patientID is not None:
            patient = self.get_patient(patientID = patientID)
            if patient is not None:
                with sqlite3.connect(DATABASE_PATH) as con:
                    cur = con.cursor()
                    cur.execute("DELETE FROM Notes WHERE patientID = ?", (patientID,))
                    con.commit()
                    return True
            else:
                return None
        note = self.get_notes(noteID=noteID)
        if note is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute("DELETE FROM Notes WHERE noteID = ?", (noteID,))
                con.commit()
                return True 
        else:
            return None
    # ------- Patient methods -----
    def pin_count(self):
        with sqlite3.connect(DATABASE_PATH) as con:
            cur = con.cursor()
            cur.execute('SELECT COUNT(*) FROM PatientDetails WHERE pinned = "True"')
            return cur.fetchone()[0]
        

    def get_patient(self, patientID = None,nodeID=None, name=None, description=None, room_num=None, pinned = None, provide_all = None):
       with sqlite3.connect(DATABASE_PATH) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # Base query and join if nodeID filter is provided
            if provide_all is not None:
                query = "SELECT * FROM PatientDetails"
                cur.execute(query)
                rows = cur.fetchall()
                print("Attempt to Fetch all pattients")
                # print(rows)
                details = []
                for i in range(0,len(rows)):
                    print("-------------------------------------")
                    print(rows[i][0])
                    print(rows[i][1])
                    print(rows[i][2])
                    print(rows[i][3])
                    details.append({'PatientID':rows[i][0], 'name': rows[i][1],'description': rows[i][2], 'room_num': rows[i][3],'pinned':rows[i][4]})
                return details
                # return entry

            if nodeID is not None:
                query = "SELECT * FROM NodeID_to_PatientID WHERE nodeID = ?"
                cur.execute(query, (nodeID,))
                entry = cur.fetchone()
                if entry is not None:
                    print(entry[1])
                    patientID = entry[1]
                    name=None
                    description = None
                    room_num = None
                    pinned = None
                else:
                    return None
            query = "SELECT pd.patientID, pd.name, pd.description, pd.room_num, pd.pinned FROM PatientDetails pd"
            conditions = []
            params = []
            print("get patient:")
            if patientID is not None:
                conditions.append("pd.patientID = ?")
                params.append(patientID)
            if name is not None:
                print("name appended")
                conditions.append("pd.name = ?")
                params.append(name)
            if description is not None:
                conditions.append("pd.description = ?")
                params.append(description)
            if room_num is not None:
                print("room num appended")
                conditions.append("pd.room_num = ?")
                params.append(room_num)
            if pinned is not None:
                print("pinned appended")
                conditions.append("pd.pinned = ?")
                params.append(str(pinned))

            if conditions:
                query += " WHERE " + " AND ".join(conditions)
                cur.execute(query, params)
                rows = cur.fetchall()
                print(rows)
                if rows != []:
                    print("Length:", len(rows))
                    details = []
                    for i in range(0,len(rows)):
                        details.append({'PatientID':rows[i][0], 'name': rows[i][1], 'description': rows[i][2],'room_num':rows[i][3], 'pinned':rows[i][4]})
                    return details
                else:
                    return None


    def get_nodeID_by_patientID(self, patientID):
        with sqlite3.connect(DATABASE_PATH) as con:
            cur = con.cursor()
            cur.execute("SELECT nodeID FROM NodeID_to_PatientID WHERE patientID = ?", (patientID,))
            result = cur.fetchone()
            return result[0] if result else None
    
    def insert_nodeid_to_patientid(self, con, nodeID, patientID):
        sql = 'INSERT INTO NodeID_to_PatientID(nodeID, patientID) VALUES(?,?)'
        cur = con.cursor(); cur.execute(sql, (nodeID, patientID)); con.commit()
        return cur.lastrowid
    
    def add_patient(self, nodeID, name, description, room_num):
        with sqlite3.connect(DATABASE_PATH) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            # pick next ID ourselves: if table empty, MAX(patientID) is NULL → COALESCE → 0 → +1 → 1
            

            # explicitly insert patientID
            name_exists = self.get_patient(name=name)
            room_num_exists = self.get_patient(room_num=room_num)
            nodeID_exists = self.get_patient(nodeID=nodeID)
            print("Add patient:")
            print("name_exists:", name_exists)
            print("room_exists:", room_num_exists)
            print("nodeID exists:", nodeID_exists)
            if name_exists is None and room_num_exists is None and nodeID_exists is None:
                cur.execute(
                    'INSERT INTO PatientDetails(patientID, name, description, room_num, pinned) '
                    'VALUES (NULL,?, ?, ?, ?)',
                    (name, description, room_num, False)
                )
                con.commit()
            #get PatientID of the newly inserted patient
                cur.execute('SELECT MAX(patientID) FROM PatientDetails')
                patientID = cur.fetchone()[0]
                self.insert_nodeid_to_patientid(con, nodeID, patientID)
                associate_device(nodeID)
                return True
            else:
                return None
    
    def edit_patient(self, patientID, name=None, description=None, room_num=None, pinned=None):
        patient = self.get_patient(patientID=patientID)
        # room_num_exists = len(self.get_patient(room_num=room_num))
        # name_exists = self.get_patient(name=name)
        if name is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT 1 FROM PatientDetails WHERE name = ? AND patientID != ?',
                    (name, patientID)
                )
                if cur.fetchone():
                    return None  # Name already used by another patient

        # Check for room_num conflict if changing
        if room_num is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'SELECT 1 FROM PatientDetails WHERE room_num = ? AND patientID != ?',
                    (room_num, patientID)
                )
                if cur.fetchone():
                    return None  # Room number already assigned to another patient

        if patient is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                updates = []
                params = []
                if name is not None:
                    updates.append("name = ?")
                    params.append(name)
                if description is not None:
                    updates.append("description = ?")
                    params.append(description)
                if room_num is not None:
                    print("Room num is not NONE!!")
                    updates.append("room_num = ?")
                    params.append(room_num)
                if pinned is not None:
                    pinned_count = self.pin_count()
                    if pinned == True and pinned_count == 3:
                        return None
                    elif pinned == False and pinned_count == 0:
                        return None
                    else:
                        updates.append("pinned = ?")
                        params.append(str(pinned))

                # add patientID as last parameter
                params.append(patientID)
                sql = f"UPDATE PatientDetails SET {', '.join(updates)} WHERE patientID = ?"
                cur.execute(sql, params)
                con.commit()
                return True
    def remove_nodeID(self,patientID):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute("DELETE FROM NodeID_to_PatientID WHERE patientID = ?", (patientID,))
                con.commit()
                return True
        else:
            return None


    def remove_patient(self,patientID):
        patient = self.get_patient(patientID=patientID)
        if patient is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                nodeID = self.get_nodeID_by_patientID(patientID)
                cur = con.cursor()
                cur.execute("PRAGMA foreign_keys = ON;")
                cur.execute("DELETE FROM PatientDetails WHERE patientID = ?", (patientID,))
                con.commit()
                self.delete_measurements_patient_records(patientID)
                self.remove_notification(patientID)
                self.remove_note(patientID)
                
                self.remove_nodeID(patientID)
                
                print("NOW I WILL INVOKE disconnect_device")
                disconnect_device(nodeID)
                return True
        else:
            return None
    # def pinned_count():
    #     with sqlite3.connect(DATABASE_PATH) as con:
    #         cur = con.cursor()
    #         cur.execute('SELECT COUNT(*) FROM PatientDetails WHERE pinned = "True"')
    #         count = cur.fetchone()[0]
    #         return count

      # ----- User methods -----   
    def get_user(self,userID = None, name=None, speciality=None, username=None, password=None):
        query = "SELECT * FROM UserData"
        conditions = []
        parameters = []

        if userID:
            conditions.append('userID = ?')
            parameters.append(userID)
        if name:
            conditions.append("name = ?")
            parameters.append(name)
        if username:
            print("appended username in get_user")
            conditions.append("username = ?")
            parameters.append(username)
        if password:
            print("appedned password in get_user")
            conditions.append("password = ?")
            parameters.append(password)
        if speciality:
            conditions.append("speciality = ?")
            parameters.append(speciality)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        with sqlite3.connect(DATABASE_PATH) as con:
            cur = con.cursor()
            cur.execute(query, parameters)
            user = cur.fetchall()
            print("User:", user)
            # print("One" + str(user))
            if user != []:
                return user
            else:
                return None

    def create_user(self, name, speciality, username, password):
        user = self.get_user(username=username, password=password)
        if user is None:
            with sqlite3.connect(DATABASE_PATH) as con:
                cur = con.cursor()
                cur.execute(
                    'INSERT INTO UserData(name, speciality, username, password) VALUES(?,?,?,?)',
                    (name, speciality, username, password)
                )
                con.commit()
                return cur.lastrowid
        else:
            return None
    
    def remove_user(self, userID):
        user = self.get_user(userID=userID)
        if user is not None:
            with sqlite3.connect(DATABASE_PATH) as con:
                con.cursor().execute("DELETE FROM UserData WHERE userID = ?", (userID,)); con.commit()
        else:
            return "{'error': 'User does not exist'}"
    
def init_app(app):
    app.cli.add_command(create_new_db)

if __name__ == "__main__":
    db = PatientDB()
    print(db.get_notifications())
    # db.add_temperature(1,28.2)
    # sleep(3)
    # db.add_temperature(1,25.2)
    # sleep(3)
    # db.add_temperature(1,11.2)
    # sleep(3)
    # db.add_bpm(1,60)
    # sleep(3)
    # db.add_bpm(1,65)

    # db.add_temperature(2,28.2)
    # db.add_temperature(2,28.2)
    # db.add_temperature(2,28.2)
    # db.add_bpm(2,60)
    # db.add_bpm(2,65)
    # print(db.get_latest_measurement_records(1,'temp',1))
    # print(db.delete_measurements_patient_records(2))
    # print(db.delete_measurements_patient_records(1))

    # print(db.remove_note(patientID=2))
    # print(db.add_bpm(1,60))
    # print(db.add_bpm(1,65))
    # print(db.remove_notification(patientID=1))
    # print(db.add_notification(1,'ordinary',True))
    # print(db.remove_note(3))
    # print(db.edit_note(5, "Updated description"))
    # db.add_patient(3,'Martin','Good condition', 30)
    # print(db.get_patient(description="New"))
    # print(db.add_patient(4,'Marti',' is awesome', 30))
    # print(db.edit_patient(2,name="Mojo",description="des", room_num=21))
    # print(db.remove_patient(2))
    # print(db.add_note(5,"This note is related to Mr.Gorov!"))
    # print(db.get_notes(patientID=1,noteID=2))
    # db.create_user(name="Mladen", speciality="Robotics", username="mladen", password="pass")
    # print(db.get_user(username="mladen",password="pass"))
    # db.remove_user(1)
    # print(db.get_user(userID=1))
    # print(db.pin_count())

    # — Patient demo —
    # pid = db.add_patient("Node123", "John Doe", "Chronic", 101, True)
    # print("New patient ID:", pid)
    # nid = db.insert_notification(pid, "emergency", False, "2025-04-03 12:00:00")
    # print("Notif ID:", nid)
    # note_id = db.insert_note(pid, "Improving.", "2025-04-03 12:05:00")
    # print("Note ID:", note_id)
    # db.edit_patient_details(pid, name="John D.", room_num=102)
    # db.add_temperature(pid, 37.5)
    # db.add_bpm(pid, 75)
    # print("Latest temps:", db.get_latest_measurement_records(pid, "temp", 5))
    # print("Details:", db.get_patient_full_details(pid))
    # db.delete_patient(pid)
    # print(f"Deleted patient {pid} and related.")

    # # — User demo —
    # user_id = db.add_user("Dr. Alice", "Cardiology", "alice", "securepass")
    # print(f"New user added with ID: {user_id}")

    # print("User details:", db.search_patients(room_num=100))
    # print("Notes:")

    # print(db.search_note(0))

    # print("Notifications:")

    # print(db.search_notification(0))
    # db.edit_patient_details(1,"Gancho")
    # print(db.get_user_details(1))

    # db.add_temperature(1,23.4)
    # db.add_temperature(1,28.2)
    # db.add_temperature(1,28.2)

    # print(db.get_latest_measurement_records(1,'bpm',1))
    # db.add_temperature(0,28.2)
    # db.add_temperature(0,28.2)
    # db.add_temperature(0,28.2)

    # db.add_temperature(1,23.4)
    # db.add_temperature(1,28.2)
    # db.add_temperature(1,28.2)
    # db.add_temperature(1,28.2)
    # db.add_temperature(1,28.2)
    # db.add_temperature(1,28.2)

    # db.add_bpm(0, 60)
    # db.add_bpm(1,65)

    # print(db.get_latest_measurement_records(0,'bpm',3))