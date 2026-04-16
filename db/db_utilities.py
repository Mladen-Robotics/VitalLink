# import sqlite3
# import os
# from datetime import datetime
# from influxdb_client import InfluxDBClient, Point
# from influxdb_client.client.write_api import SYNCHRONOUS



# DB_FILENAME = "patient_data.db"
# class PatientDB:
#     def __init__(self):
#         if not os.path.isfile(DB_FILENAME):
#             self.create_new_db()
#         self.client = InfluxDBClient(
#             url='http://localhost:8086',
#             token='r2xnS1k57vPE_i1mgpINBHIwIuTb_ELtzDn8NHrV9hbXFY0ge_PRD3cTQFu7TyC3EG2K4XKfP8NKPd1R-9LtJw==',
#             org='Robo'
#         )
#         self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
#         self.query_api = self.client.query_api()
#         self.delete_api = self.client.delete_api()
#     def add_temperature(self,patient_id, temperature):
#         point = Point("temp").tag("PatientID", patient_id).field("temp", temperature)
#         self.write_api.write(bucket="patient_measurments", org='Robo', record=point)
#         print(f"Temperature {temperature} added for PatientID {patient_id}.")

# # Function to add a BPM measurement for a given PatientID
#     def add_bpm(self,patient_id, bpm):
#         point = Point("bpm").tag("PatientID", patient_id).field("bpm", bpm)
#         self.write_api.write(bucket="patient_measurments", org='Robo', record=point)
#         print(f"BPM {bpm} added for PatientID {patient_id}.")

#     def delete_measurments_patient_records(self,patient_id):
#         start = "1970-01-01T00:00:00Z"
#         stop = datetime.utcnow().isoformat() + "Z"
#         predicate = f'PatientID="{patient_id}"'
#         self.delete_api.delete(start, stop, predicate, bucket="patient_measurments", org='Robo')
#         print(f"All records for PatientID {patient_id} have been deleted.")

#     def get_latest_measurment_records(self,patient_id, measurement, n):
#         query = f'''
#         from(bucket: "patient_measurments")
#         |> range(start: 0)
#         |> filter(fn: (r) => r["_measurement"] == "{measurement}")
#         |> filter(fn: (r) => r["PatientID"] == "{patient_id}")
#         |> sort(columns: ["_time"], desc: true)
#         |> limit(n: {n})
#         '''
#         result = self.query_api.query(org='Robo', query=query)
#         records = []
#         for table in result:
#             for record in table.records:
#                 records.append({
#                     "time": record.get_time(),
#                     "measurement": record.get_measurement(),
#                     "field": record.get_field(),
#                     "value": record.get_value()
#                 })
#         return records

#     def create_new_db(self):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             print("Database was successfully created!")
#             cur.execute("PRAGMA foreign_keys = ON;")
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS PatientDetails (
#                     patientID INTEGER PRIMARY KEY,
#                     name TEXT,
#                     description TEXT,
#                     room_num INTEGER,
#                     pinned BOOLEAN
#                 );
#             ''')
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS NodeID_to_PatientID (
#                     nodeID TEXT NOT NULL,
#                     patientID INTEGER NOT NULL,
#                     PRIMARY KEY (nodeID, patientID),
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS Notifications (
#                     notificationID INTEGER PRIMARY KEY,
#                     patientID INTEGER NOT NULL,
#                     type TEXT CHECK(type IN ('emergency','ordinary')),
#                     confirmed BOOLEAN,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS Notes (
#                     noteID INTEGER PRIMARY KEY ,
#                     patientID INTEGER NOT NULL,
#                     description TEXT,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             con.commit()

#     def insert_nodeid_to_patientid(self, con, nodeID, patientID):
#         sql = '''INSERT INTO NodeID_to_PatientID(nodeID, patientID) VALUES(?,?)'''
#         cur = con.cursor()
#         cur.execute(sql, (nodeID, patientID))
#         con.commit()
#         return cur.lastrowid

#     def add_patient(self, nodeID, name, description, room_num, pinned):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             sql = '''INSERT INTO PatientDetails(name, description, room_num, pinned)
#                      VALUES(?,?,?,?)'''
#             cur.execute(sql, (name, description, room_num, pinned))
#             con.commit()
#             patientID = cur.lastrowid
#             self.insert_nodeid_to_patientid(con, nodeID, patientID)
#             return patientID

#     def delete_patient(self, patientID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             cur.execute("PRAGMA foreign_keys = ON;")
#             sql = '''DELETE FROM PatientDetails WHERE patientID = ?'''
#             cur.execute(sql, (patientID,))
#             con.commit()
#             self.delete_measurments_patient_records(patientID)

#              # # Removing a notification
#             db.remove_notification(patientID)
#             # # Removing a note
#             db.remove_note(patientID)

#     def remove_notification(self, notificationID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             sql = '''DELETE FROM Notifications WHERE notificationID = ?'''
#             cur.execute(sql, (notificationID,))
#             con.commit()

#     def remove_note(self, noteID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             sql = '''DELETE FROM Notes WHERE noteID = ?'''
#             cur.execute(sql, (noteID,))
#             con.commit()

#     def edit_patient_details(self, patientID, name=None, description=None, room_num=None, pinned=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             updates = []
#             params = []
#             if name is not None:
#                 updates.append("name = ?")
#                 params.append(name)
#             if description is not None:
#                 updates.append("description = ?")
#                 params.append(description)
#             if room_num is not None:
#                 updates.append("room_num = ?")
#                 params.append(room_num)
#             if pinned is not None:
#                 updates.append("pinned = ?")
#                 params.append(pinned)
#             params.append(patientID)
#             sql = f'''UPDATE PatientDetails SET {', '.join(updates)} WHERE patientID = ?'''
#             cur.execute(sql, params)
#             con.commit()

#     def edit_notification(self, notificationID, n_type=None, confirmed=None, timestamp=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             updates = []
#             params = []
#             if n_type is not None:
#                 updates.append("type = ?")
#                 params.append(n_type)
#             if confirmed is not None:
#                 updates.append("confirmed = ?")
#                 params.append(confirmed)
#             if timestamp is not None:
#                 updates.append("timestamp = ?")
#                 params.append(timestamp)
#             params.append(notificationID)
#             sql = f'''UPDATE Notifications SET {', '.join(updates)} WHERE notificationID = ?'''
#             cur.execute(sql, params)
#             con.commit()

#     def edit_note(self, noteID, description=None, timestamp=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             updates = []
#             params = []
#             if description is not None:
#                 updates.append("description = ?")
#                 params.append(description)
#             if timestamp is not None:
#                 updates.append("timestamp = ?")
#                 params.append(timestamp)
#             params.append(noteID)
#             sql = f'''UPDATE Notes SET {', '.join(updates)} WHERE noteID = ?'''
#             cur.execute(sql, params)
#             con.commit()

#     def insert_notification(self, patientID, n_type, confirmed, timestamp):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             sql = '''INSERT INTO Notifications(patientID, type, confirmed, timestamp)
#                     VALUES(?,?,?,?)'''
#             cur.execute(sql, (patientID, n_type, confirmed, timestamp))
#             con.commit()
#             return cur.lastrowid

#     def insert_note(self,patientID, description, timestamp):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             sql = '''INSERT INTO Notes(patientID, description, timestamp)
#                     VALUES(?,?,?)'''
#             cur.execute(sql, (patientID, description, timestamp))
#             con.commit()
#             return cur.lastrowid
#     def get_patient_full_details(self, patientID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()

#             # Fetch patient details
#             cur.execute('''
#                 SELECT patientID, name, description, room_num, pinned
#                 FROM PatientDetails
#                 WHERE patientID = ?
#             ''', (patientID,))
#             patient = cur.fetchone()
#             if not patient:
#                 return None

#             # Fetch associated node IDs
#             cur.execute('''
#                 SELECT nodeID
#                 FROM NodeID_to_PatientID
#                 WHERE patientID = ?
#             ''', (patientID,))
#             node_ids = [row[0] for row in cur.fetchall()]

#             # Fetch notifications
#             cur.execute('''
#                 SELECT notificationID, type, confirmed, timestamp
#                 FROM Notifications
#                 WHERE patientID = ?
#             ''', (patientID,))
#             notifications = [
#                 {
#                     "notificationID": row[0],
#                     "type": row[1],
#                     "confirmed": bool(row[2]),
#                     "timestamp": row[3]
#                 }
#                 for row in cur.fetchall()
#             ]

#             # Fetch notes
#             cur.execute('''
#                 SELECT noteID, description, timestamp
#                 FROM Notes
#                 WHERE patientID = ?
#             ''', (patientID,))
#             notes = [
#                 {
#                     "noteID": row[0],
#                     "description": row[1],
#                     "timestamp": row[2]
#                 }
#                 for row in cur.fetchall()
#             ]

#             return {
#                 "patientID": patient[0],
#                 "name": patient[1],
#                 "description": patient[2],
#                 "room_num": patient[3],
#                 "pinned": bool(patient[4]),
#                 "nodeIDs": node_ids,
#                 "notifications": notifications,
#                 "notes": notes
#             }


# # if __name__ == '__main__':
# #     db = PatientDB()
# #     # Example usage:
# #     new_patient_id = db.add_patient("Node123", "John Doe", "Patient with chronic condition", 101, True)
# #     print("New patient added with ID:", new_patient_id)
# #     notification_id = insert_notification(new_patient_id, "emergency", False, "2025-04-03 12:00:00")
# #     # print("Notification added with ID:", notification_id)
# #     note_id = insert_note(new_patient_id, "Patient shows signs of improvement.", "2025-04-03 12:05:00")
# #     print("Note added with ID:", note_id)
# #     # # Editing patient details
# #     db.edit_patient_details(new_patient_id, name="Johnathan Doe", room_num=102)
# #     # # # Removing a notification
# #     # db.remove_notification(notification_id)
# #     # # # Removing a note
# #     # db.remove_note(note_id)
# #     # Deleting the patient and all related records
# #     db.delete_patient(new_patient_id)
 
# if __name__ == "__main__":
#     # Create a PatientDB instance to interact with SQLite and InfluxDB
#     db = PatientDB()

#     # 1. Adding a new patient
#     patient_id = db.add_patient("Node123", "John Doe", "Patient with chronic condition", 101, True)
#     print(f"New patient added with ID: {patient_id}")

#     # 2. Inserting a notification
#     notification_id = db.insert_notification(patient_id, "emergency", False, "2025-04-03 12:00:00")
#     print(f"Notification added with ID: {notification_id}")

#     # 3. Inserting a note
#     note_id = db.insert_note(patient_id, "Patient shows signs of improvement.", "2025-04-03 12:05:00")
#     print(f"Note added with ID: {note_id}")

#     # 4. Editing patient details
#     db.edit_patient_details(patient_id, name="Johnathan Doe", room_num=102)
#     print("Patient details updated.")

#     # 5. Removing the notification
#     # db.remove_notification(notification_id)
#     # print(f"Notification {notification_id} removed.")

#     # # # 6. Removing the note
#     # db.remove_note(note_id)
#     # print(f"Note {note_id} removed.")

#     # # 7. Deleting the patient and all related records
#     db.add_temperature(patient_id, 37.5)
#     print(f"Temperature for patient {patient_id} added.")

#     # 9. Adding BPM
#     db.add_bpm(patient_id, 75)
#     print(f"BPM for patient {patient_id} added.")

#     measurements = db.get_latest_measurment_records(patient_id, "temp", 5)
#     print(f"Latest measurements for patient {patient_id}: {measurements}")

#     details = db.get_patient_full_details(patient_id)
#     print("Patient detaills:", details)

#     db.delete_patient(patient_id)
#     print(f"Patient {patient_id} and all related records deleted.")

#     # Interacting with InfluxDB
#     # 8. Adding temperature
    

#     # 10. Deleting all measurements for the patient from InfluxDB
#     # db.delete_measurments_patient_records(patient_id)
#     print(f"All records for patient {patient_id} deleted from InfluxDB.")

#     # 11. Querying the latest measurements
#     measurements = db.get_latest_measurment_records(patient_id, "temp", 5)
#     print(f"Latest measurements for patient {patient_id}: {measurements}")



# import sqlite3
# import os
# from datetime import datetime
# from influxdb_client import InfluxDBClient, Point
# from influxdb_client.client.write_api import SYNCHRONOUS

# DB_FILENAME = "patient_data.db"

# class PatientDB:
#     def __init__(self):
#         if not os.path.isfile(DB_FILENAME):
#             self.create_new_db()
#         self.client = InfluxDBClient(
#             url='http://localhost:8086',
#             token='r2xnS1k57vPE_i1mgpINBHIwIuTb_ELtzDn8NHrV9hbXFY0ge_PRD3cTQFu7TyC3EG2K4XKfP8NKPd1R-9LtJw==',
#             org='Robo'
#         )
#         self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
#         self.query_api = self.client.query_api()
#         self.delete_api = self.client.delete_api()

#     def add_temperature(self, patient_id, temperature):
#         point = Point("temp").tag("PatientID", patient_id).field("temp", temperature)
#         self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
#         print(f"Temperature {temperature} added for PatientID {patient_id}.")

#     def add_bpm(self, patient_id, bpm):
#         point = Point("bpm").tag("PatientID", patient_id).field("bpm", bpm)
#         self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
#         print(f"BPM {bpm} added for PatientID {patient_id}.")

#     def delete_measurements_patient_records(self, patient_id):
#         start = "1970-01-01T00:00:00Z"
#         stop = datetime.utcnow().isoformat() + "Z"
#         predicate = f'PatientID="{patient_id}"'
#         self.delete_api.delete(start, stop, predicate, bucket="patient_measurements", org='Robo')
#         print(f"All records for PatientID {patient_id} have been deleted.")

#     def get_latest_measurement_records(self, patient_id, measurement, n):
#         query = f'''
#         from(bucket: "patient_measurements")
#         |> range(start: 0)
#         |> filter(fn: (r) => r["_measurement"] == "{measurement}")
#         |> filter(fn: (r) => r["PatientID"] == "{patient_id}")
#         |> sort(columns: ["_time"], desc: true)
#         |> limit(n: {n})
#         '''
#         result = self.query_api.query(org='Robo', query=query)
#         records = []
#         for table in result:
#             for record in table.records:
#                 records.append({
#                     "time": record.get_time(),
#                     "measurement": record.get_measurement(),
#                     "field": record.get_field(),
#                     "value": record.get_value()
#                 })
#         return records

#     def create_new_db(self):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             print("Database was successfully created!")
#             cur.execute("PRAGMA foreign_keys = ON;")
#             # Patients
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS PatientDetails (
#                     patientID INTEGER PRIMARY KEY,
#                     name TEXT,
#                     description TEXT,
#                     room_num INTEGER,
#                     pinned BOOLEAN
#                 );
#             ''')
#             # Node mappings
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS NodeID_to_PatientID (
#                     nodeID TEXT NOT NULL,
#                     patientID INTEGER NOT NULL,
#                     PRIMARY KEY (nodeID, patientID),
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             # Notifications
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS Notifications (
#                     notificationID INTEGER PRIMARY KEY,
#                     patientID INTEGER NOT NULL,
#                     type TEXT CHECK(type IN ('emergency','ordinary')),
#                     confirmed BOOLEAN,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             # Notes
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS Notes (
#                     noteID INTEGER PRIMARY KEY,
#                     patientID INTEGER NOT NULL,
#                     description TEXT,
#                     timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#                     FOREIGN KEY (patientID) REFERENCES PatientDetails(patientID) ON DELETE CASCADE
#                 );
#             ''')
#             # User data
#             cur.execute('''
#                 CREATE TABLE IF NOT EXISTS UserData (
#                     userID INTEGER PRIMARY KEY,
#                     name TEXT,
#                     speciality TEXT,
#                     username TEXT,
#                     password TEXT
#                 );
#             ''')
#             con.commit()

#     # ----- Patient methods -----
#     def insert_nodeid_to_patientid(self, con, nodeID, patientID):
#         sql = '''INSERT INTO NodeID_to_PatientID(nodeID, patientID) VALUES(?,?)'''
#         cur = con.cursor(); cur.execute(sql, (nodeID, patientID)); con.commit()
#         return cur.lastrowid

#     def add_patient(self, nodeID, name, description, room_num, pinned):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             cur.execute(
#                 'INSERT INTO PatientDetails(name, description, room_num, pinned) VALUES(?,?,?,?)',
#                 (name, description, room_num, pinned)
#             )
#             con.commit()
#             pid = cur.lastrowid
#             self.insert_nodeid_to_patientid(con, nodeID, pid)
#             return pid

#     def delete_patient(self, patientID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor(); cur.execute("PRAGMA foreign_keys = ON;"); cur.execute(
#                 "DELETE FROM PatientDetails WHERE patientID = ?", (patientID,)
#             ); con.commit()
#         self.delete_measurements_patient_records(patientID)
#         self.remove_notification(patientID)
#         self.remove_note(patientID)

#     # ----- Notification & Note -----
#     def remove_notification(self, notificationID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             con.cursor().execute("DELETE FROM Notifications WHERE notificationID = ?", (notificationID,)); con.commit()

#     def remove_note(self, noteID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             con.cursor().execute("DELETE FROM Notes WHERE noteID = ?", (noteID,)); con.commit()

#     # ----- Patient edits -----
#     def edit_patient_details(self, patientID, name=None, description=None, room_num=None, pinned=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             updates, params = [], []
#             if name: updates.append("name = ?"); params.append(name)
#             if description: updates.append("description = ?"); params.append(description)
#             if room_num: updates.append("room_num = ?"); params.append(room_num)
#             if pinned is not None: updates.append("pinned = ?"); params.append(pinned)
#             params.append(patientID)
#             con.cursor().execute(f"UPDATE PatientDetails SET {', '.join(updates)} WHERE patientID = ?", params)
#             con.commit()

#     # ----- Notification & Note edits -----
#     def edit_notification(self, notificationID, n_type=None, confirmed=None, timestamp=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             updates, params = [], []
#             if n_type: updates.append("type = ?"); params.append(n_type)
#             if confirmed is not None: updates.append("confirmed = ?"); params.append(confirmed)
#             if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
#             params.append(notificationID)
#             con.cursor().execute(f"UPDATE Notifications SET {', '.join(updates)} WHERE notificationID = ?", params)
#             con.commit()

#     def edit_note(self, noteID, description=None, timestamp=None):
#         with sqlite3.connect(DB_FILENAME) as con:
#             updates, params = [], []
#             if description: updates.append("description = ?"); params.append(description)
#             if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
#             params.append(noteID)
#             con.cursor().execute(f"UPDATE Notes SET {', '.join(updates)} WHERE noteID = ?", params)
#             con.commit()

#     # ----- Measurements queries -----
#     def insert_notification(self, patientID, n_type, confirmed, timestamp):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor(); cur.execute(
#                 'INSERT INTO Notifications(patientID, type, confirmed, timestamp) VALUES(?,?,?,?)',
#                 (patientID, n_type, confirmed, timestamp)
#             ); con.commit(); return cur.lastrowid

#     def insert_note(self, patientID, description, timestamp):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor(); cur.execute(
#                 'INSERT INTO Notes(patientID, description, timestamp) VALUES(?,?,?)',
#                 (patientID, description, timestamp)
#             ); con.commit(); return cur.lastrowid

#     # ----- User methods -----
#     def add_user(self, name, speciality, username, password):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             cur.execute(
#                 'INSERT INTO UserData(name, speciality, username, password) VALUES(?,?,?,?)',
#                 (name, speciality, username, password)
#             )
#             con.commit()
#             return cur.lastrowid

#     def remove_user(self, userID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             con.cursor().execute("DELETE FROM UserData WHERE userID = ?", (userID,)); con.commit()

#     # ----- Fetch full details -----
#     def get_patient_full_details(self, patientID):
#         with sqlite3.connect(DB_FILENAME) as con:
#             cur = con.cursor()
#             cur.execute(
#                 'SELECT patientID, name, description, room_num, pinned FROM PatientDetails WHERE patientID = ?',
#                 (patientID,)
#             )
#             patient = cur.fetchone()
#             if not patient: return None
#             cur.execute('SELECT nodeID FROM NodeID_to_PatientID WHERE patientID = ?', (patientID,))
#             node_ids = [r[0] for r in cur.fetchall()]
#             cur.execute(
#                 'SELECT notificationID, type, confirmed, timestamp FROM Notifications WHERE patientID = ?',
#                 (patientID,)
#             )
#             notifications = [{
#                 "notificationID": r[0], "type": r[1], "confirmed": bool(r[2]), "timestamp": r[3]
#             } for r in cur.fetchall()]
#             cur.execute('SELECT noteID, description, timestamp FROM Notes WHERE patientID = ?', (patientID,))
#             notes = [{"noteID": r[0], "description": r[1], "timestamp": r[2]} for r in cur.fetchall()]
#             return {
#                 "patientID": patient[0], "name": patient[1], "description": patient[2],
#                 "room_num": patient[3], "pinned": bool(patient[4]),
#                 "nodeIDs": node_ids, "notifications": notifications, "notes": notes
#             }
#         def get_user_details(self, userID):
#             with sqlite3.connect(DB_FILENAME) as con:
#                 cur = con.cursor()
#                 cur.execute(
#                     'SELECT userID, name, speciality, username, password FROM UserData WHERE userID = ?',
#                     (userID,)
#                 )
#                 user = cur.fetchone()
#                 if user:
#                     return {
#                         "userID": user[0],
#                         "name": user[1],
#                         "speciality": user[2],
#                         "username": user[3],
#                         "password": user[4]
#                     }
#                 return None


# if __name__ == "__main__":
#     db = PatientDB()
#     # Patient demo
#     pid = db.add_patient("Node123", "John Doe", "Chronic", 101, True)
#     print("New patient ID:", pid)
#     nid = db.insert_notification(pid, "emergency", False, "2025-04-03 12:00:00")
#     print("Notif ID:", nid)
#     note_id = db.insert_note(pid, "Improving.", "2025-04-03 12:05:00")
#     print("Note ID:", note_id)
#     db.edit_patient_details(pid, name="John D.", room_num=102)
#     db.add_temperature(pid, 37.5)
#     db.add_bpm(pid, 75)
#     print("Latest temps:", db.get_latest_measurement_records(pid, "temp", 5))
#     print("Details:", db.get_patient_full_details(pid))
#     db.delete_patient(pid)
#     print(f"Deleted patient {pid} and related.")

#     # User demo
#     user_id = db.add_user("Dr. Alice", "Cardiology", "alice", "securepass")
#     print(f"New user added with ID: {user_id}")
#     details = db.get_user_details(user_id)
#     db.remove_user(user_id)
#     print(f"User {user_id} removed.")

import sqlite3
import os
from datetime import datetime
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

DB_FILENAME = "patient_data.db"

class PatientDB:
    def __init__(self):
        if not os.path.isfile(DB_FILENAME):
            self.create_new_db()
        self.client = InfluxDBClient(
            url='http://localhost:8086',
            token='r2xnS1k57vPE_i1mgpINBHIwIuTb_ELtzDn8NHrV9hbXFY0ge_PRD3cTQFu7TyC3EG2K4XKfP8NKPd1R-9LtJw==',
            org='Robo'
        )
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()
        self.delete_api = self.client.delete_api()

    def add_temperature(self, patient_id, temperature):
        point = Point("temp").tag("PatientID", patient_id).field("temp", temperature)
        self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
        print(f"Temperature {temperature} added for PatientID {patient_id}.")

    def add_bpm(self, patient_id, bpm):
        point = Point("bpm").tag("PatientID", patient_id).field("bpm", bpm)
        self.write_api.write(bucket="patient_measurements", org='Robo', record=point)
        print(f"BPM {bpm} added for PatientID {patient_id}.")

    def delete_measurements_patient_records(self, patient_id):
        start = "1970-01-01T00:00:00Z"
        stop = datetime.utcnow().isoformat() + "Z"
        predicate = f'PatientID="{patient_id}"'
        self.delete_api.delete(start, stop, predicate, bucket="patient_measurements", org='Robo')
        print(f"All records for PatientID {patient_id} have been deleted.")

    def get_latest_measurement_records(self, patient_id, measurement, n):
        query = f'''
        from(bucket: "patient_measurements")
        |> range(start: 0)
        |> filter(fn: (r) => r["_measurement"] == "{measurement}")
        |> filter(fn: (r) => r["PatientID"] == "{patient_id}")
        |> sort(columns: ["_time"], desc: true)
        |> limit(n: {n})
        '''
        result = self.query_api.query(org='Robo', query=query)
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

    def create_new_db(self):
        with sqlite3.connect(DB_FILENAME) as con:
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
            ''')  # INTEGER PRIMARY KEY ще автоинкрементира и ще попълва дупки :contentReference[oaicite:0]{index=0}

            con.commit()

    # ----- Patient methods -----
    def insert_nodeid_to_patientid(self, con, nodeID, patientID):
        sql = 'INSERT INTO NodeID_to_PatientID(nodeID, patientID) VALUES(?,?)'
        cur = con.cursor(); cur.execute(sql, (nodeID, patientID)); con.commit()
        return cur.lastrowid

    def add_patient(self, nodeID, name, description, room_num, pinned):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO PatientDetails(name, description, room_num, pinned) VALUES(?,?,?,?)',
                (name, description, room_num, pinned)
            )
            con.commit()
            pid = cur.lastrowid
            self.insert_nodeid_to_patientid(con, nodeID, pid)  # parameterized insert :contentReference[oaicite:1]{index=1}
            return pid

    def delete_patient(self, patientID):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute("PRAGMA foreign_keys = ON;")
            cur.execute("DELETE FROM PatientDetails WHERE patientID = ?", (patientID,))  # safe DELETE :contentReference[oaicite:2]{index=2}
            con.commit()
        self.delete_measurements_patient_records(patientID)
        self.remove_notification(patientID)
        self.remove_note(patientID)

    # ----- Notification & Note -----
    def remove_notification(self, notificationID):
        with sqlite3.connect(DB_FILENAME) as con:
            con.cursor().execute("DELETE FROM Notifications WHERE notificationID = ?", (notificationID,)); con.commit()

    def remove_note(self, noteID):
        with sqlite3.connect(DB_FILENAME) as con:
            con.cursor().execute("DELETE FROM Notes WHERE noteID = ?", (noteID,)); con.commit()

    # ----- Patient edits -----
    def edit_patient_details(self, patientID, name=None, description=None, room_num=None, pinned=None):
        with sqlite3.connect(DB_FILENAME) as con:
            updates, params = [], []
            if name: updates.append("name = ?"); params.append(name)
            if description: updates.append("description = ?"); params.append(description)
            if room_num: updates.append("room_num = ?"); params.append(room_num)
            if pinned is not None: updates.append("pinned = ?"); params.append(pinned)
            params.append(patientID)
            con.cursor().execute(f"UPDATE PatientDetails SET {', '.join(updates)} WHERE patientID = ?", params)
            con.commit()

    # ----- Notification & Note edits -----
    def edit_notification(self, notificationID, n_type=None, confirmed=None, timestamp=None):
        with sqlite3.connect(DB_FILENAME) as con:
            updates, params = [], []
            if n_type: updates.append("type = ?"); params.append(n_type)
            if confirmed is not None: updates.append("confirmed = ?"); params.append(confirmed)
            if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
            params.append(notificationID)
            con.cursor().execute(f"UPDATE Notifications SET {', '.join(updates)} WHERE notificationID = ?", params)
            con.commit()

    def edit_note(self, noteID, description=None, timestamp=None):
        with sqlite3.connect(DB_FILENAME) as con:
            updates, params = [], []
            if description: updates.append("description = ?"); params.append(description)
            if timestamp: updates.append("timestamp = ?"); params.append(timestamp)
            params.append(noteID)
            con.cursor().execute(f"UPDATE Notes SET {', '.join(updates)} WHERE noteID = ?", params)
            con.commit()

    # ----- Measurement inserts -----
    def insert_notification(self, patientID, n_type, confirmed, timestamp):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO Notifications(patientID, type, confirmed, timestamp) VALUES(?,?,?,?)',
                (patientID, n_type, confirmed, timestamp)
            )
            con.commit()
            return cur.lastrowid

    def insert_note(self, patientID, description, timestamp):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO Notes(patientID, description, timestamp) VALUES(?,?,?)',
                (patientID, description, timestamp)
            )
            con.commit()
            return cur.lastrowid

    # ----- User methods -----
    def add_user(self, name, speciality, username, password):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute(
                'INSERT INTO UserData(name, speciality, username, password) VALUES(?,?,?,?)',
                (name, speciality, username, password)
            )  # параметризирано INSERT :contentReference[oaicite:3]{index=3}
            con.commit()
            return cur.lastrowid

    def remove_user(self, userID):
        with sqlite3.connect(DB_FILENAME) as con:
            con.cursor().execute("DELETE FROM UserData WHERE userID = ?", (userID,)); con.commit()  # безопасно DELETE :contentReference[oaicite:4]{index=4}

    def get_user_details(self, userID):
        with sqlite3.connect(DB_FILENAME) as con:
            con.row_factory = sqlite3.Row  # връщаме Row обект за по-удобен достъп :contentReference[oaicite:5]{index=5}
            cur = con.cursor()
            cur.execute(
                'SELECT userID, name, speciality, username, password FROM UserData WHERE userID = ?',
                (userID,)
            )
            row = cur.fetchone()  # fetchone връща tuple/Row :contentReference[oaicite:6]{index=6}
            if row:
                return dict(row)
            return None

    def get_user_by_credentials(self, username, password):
        with sqlite3.connect(DB_FILENAME) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                'SELECT userID, name, speciality, username FROM UserData WHERE username = ? AND password = ?',
                (username, password)  # пароли в чист текст – за production hash! :contentReference[oaicite:7]{index=7}
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None

    # ----- Fetch full patient details -----
    def get_patient_full_details(self, patientID):
        with sqlite3.connect(DB_FILENAME) as con:
            cur = con.cursor()
            cur.execute(
                'SELECT patientID, name, description, room_num, pinned FROM PatientDetails WHERE patientID = ?',
                (patientID,)
            )
            patient = cur.fetchone()
            if not patient:
                return None
            cur.execute('SELECT nodeID FROM NodeID_to_PatientID WHERE patientID = ?', (patientID,))
            node_ids = [r[0] for r in cur.fetchall()]
            cur.execute(
                'SELECT notificationID, type, confirmed, timestamp FROM Notifications WHERE patientID = ?',
                (patientID,)
            )
            notifications = [{
                "notificationID": r[0], "type": r[1], "confirmed": bool(r[2]), "timestamp": r[3]
            } for r in cur.fetchall()]
            cur.execute('SELECT noteID, description, timestamp FROM Notes WHERE patientID = ?', (patientID,))
            notes = [{"noteID": r[0], "description": r[1], "timestamp": r[2]} for r in cur.fetchall()]
            return {
                "patientID": patient[0], "name": patient[1], "description": patient[2],
                "room_num": patient[3], "pinned": bool(patient[4]),
                "nodeIDs": node_ids, "notifications": notifications, "notes": notes
            }

if __name__ == "__main__":
    db = PatientDB()

    # — Patient demo —
    pid = db.add_patient("Node123", "John Doe", "Chronic", 101, True)
    print("New patient ID:", pid)
    nid = db.insert_notification(pid, "emergency", False, "2025-04-03 12:00:00")
    print("Notif ID:", nid)
    note_id = db.insert_note(pid, "Improving.", "2025-04-03 12:05:00")
    print("Note ID:", note_id)
    db.edit_patient_details(pid, name="John D.", room_num=102)
    db.add_temperature(pid, 37.5)
    db.add_bpm(pid, 75)
    print("Latest temps:", db.get_latest_measurement_records(pid, "temp", 5))
    print("Details:", db.get_patient_full_details(pid))
    db.delete_patient(pid)
    print(f"Deleted patient {pid} and related.")

    # — User demo —
    user_id = db.add_user("Dr. Alice", "Cardiology", "alice", "securepass")
    print(f"New user added with ID: {user_id}")
    print("User details:", db.get_user_details(user_id))
    auth = db.get_user_by_credentials("alice", "securepass")
    print("Authenticated user:", auth)
    db.remove_user(user_id)
    print(f"User {user_id} removed.")
