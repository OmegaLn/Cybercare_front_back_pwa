from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3


class Event(Resource):
    TABLE_NAME = 'events'

    parser = reqparse.RequestParser()
    # Add argument date
    parser.add_argument('name',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('date',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('lieu',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('objet',
        type=str,
        required=True,
        help="This field cannot be left blank!"
    )


    @jwt_required()
    def get(self, name):
        event = self.find_by_name(name)
        if event:
            return event
        return {'message': 'Event not found'}, 404

    @classmethod
    def find_by_name(cls, name):
        #Find an event by its name
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table} WHERE name=?".format(table=cls.TABLE_NAME)
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        connection.close()

        if row:
            return {'event': {'name': row[0], 'date': row[1], 'lieu': row[2]}}

    def post(self, name):
        if self.find_by_name(name):
            return {'message': "An event with name '{}' already exists.".format(name)}

        data = Event.parser.parse_args()

        event = {'name': name, 'date': data['date'], 'lieu': data['lieu'], 'objet': data['objet'] }

        try:
            Event.insert(event)
        except:
            return {"message": "An error occurred inserting the event."}

        return event

    @classmethod
    def insert(cls, event):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "INSERT INTO {table} VALUES(?, ?, ?, ?)".format(table=cls.TABLE_NAME)
        cursor.execute(query, (event['name'], event['date'], event['lieu'], event['objet']))

        connection.commit()
        connection.close()

    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Event deleted'}

    @jwt_required()
    def put(self, name):
        data = Event.parser.parse_args()
        event = self.find_by_name(name)
        updated_event = {'name': name, 'date': data['date'], 'lieu': ['lieu'], 'objet': ['objet']}
        if event is None:
            try:
                Event.insert(updated_event)
            except:
                return {"message": "An error occurred inserting the event."}
        else:
            try:
                Event.update(updated_event)
            except:
                raise
                return {"message": "An error occurred updating the event."}
        return updated_event

    @classmethod
    def update(cls, event):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "UPDATE {table} SET date=? WHERE name=?".format(table=cls.TABLE_NAME)
        cursor.execute(query, (event['date'], event['name']))

        connection.commit()
        connection.close()


class EventList(Resource):
    TABLE_NAME = 'events'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        events = []
        for row in result:
            events.append({'name': row[0], 'date': row[1], 'lieu': row[2], 'objet': row[3]})
        connection.close()

        return {'events': events, 'status': 'SUCCESS'}