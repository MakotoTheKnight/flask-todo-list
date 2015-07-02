import sqlite3

from sqlite3 import IntegrityError


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('todo.db', check_same_thread=False)
        self.cursor = self.connection.cursor()

    def create_list(self, list_name):
        try:
            self.cursor.execute('PRAGMA foreign_keys = ON')
            r = self.cursor.execute('INSERT INTO list (name) VALUES (?)', (list_name,))
            self.connection.commit()
            return r
        except IntegrityError as e:
            return False

    def create_entry(self, list_name, text):
        if not text:
            return False
        try:
            list_id = self.__find_id_of_list(list_name)
            self.cursor.execute('PRAGMA foreign_keys = ON')
            r = self.cursor.execute('INSERT INTO entry (text, list_id) VALUES (?, ?)', (text, list_id))
            self.connection.commit()
            return r
        except IntegrityError as e:
            return False

    def update_entry(self, list_name, entry_id, data):
        try:
            has_updated = False
            list_id = self.__find_id_of_list(list_name)
            self.cursor.execute('PRAGMA foreign_keys = ON')
            e = self.cursor.execute('SELECT * FROM entry WHERE id = (?)', (entry_id,)).fetchone()
            if not e:
                return False  # no entries
            entry = dict(zip(
                ('id', 'text', 'completed', 'list_id'),
                e))
            if entry['list_id'] != list_id:
                return False  # Updating the wrong thing
            else:
                entry.update(data)
                for key, value in data.iteritems():
                    self.cursor.execute('PRAGMA foreign_keys = ON')
                    self.cursor.execute('UPDATE entry SET {} = ? WHERE id = (?)'.format(key), (value, entry_id))
                    has_updated = True
                self.connection.commit()
                return entry if has_updated else {}
        except Exception as e:
            print e.message
            return False

    def delete_entry(self, list_name, entry_id):
        try:
            list_id = self.__find_id_of_list(list_name)
            self.cursor.execute('PRAGMA foreign_keys = ON')
            self.cursor.execute('DELETE FROM entry WHERE id = (?) AND list_id = (?)', (entry_id, list_id))
            self.connection.commit()
            return True
        except Exception as e:
            print e.message
            return False

    def list_all(self):
        l = self.cursor.execute('SELECT * FROM list').fetchall()
        container = dict()
        container['lists'] = []
        for row in l:
            r = dict(zip(('id', 'name'), row))
            entries = self.list_entries(r['name'])
            r.update(entries)
            container['lists'].append(r)

        return container

    def list_entries(self, list_name):
        self.cursor.execute('PRAGMA foreign_keys = ON')
        l = self.cursor.execute(
            'SELECT e.* FROM list l ' +
            'LEFT JOIN entry e ON e.list_id = l.id WHERE l.name = (?)',
            (list_name,))

        container = dict()
        container['entries'] = []
        for row in l:
            r = dict(zip(('id', 'text', 'completed'), row))
            r['completed'] = bool(r['completed'])
            container['entries'].append(r)

        return container

    def __find_id_of_list(self, list_name):
        self.cursor.execute('PRAGMA foreign_keys = ON')
        r = self.cursor.execute('SELECT id FROM list WHERE name = (?)', (list_name,))
        return r.fetchone()[0]
