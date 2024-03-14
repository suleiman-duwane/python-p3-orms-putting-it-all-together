import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    db = 'dogs.db'

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  
    @classmethod
    def create_table(cls):
        conn = sqlite3.connect(cls.db)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS dogs
                     (id INTEGER PRIMARY KEY, name TEXT, breed TEXT)''')
        conn.commit()
        conn.close()

    @classmethod
    def drop_table(cls):
        conn = sqlite3.connect(cls.db)
        c = conn.cursor()
        c.execute('''DROP TABLE IF EXISTS dogs''')
        conn.commit()
        conn.close()

    def save(self):
        if self.id is None:
            with sqlite3.connect(self.db) as conn:
                c = conn.cursor()
                c.execute('''INSERT INTO dogs (name, breed) VALUES (?, ?)''', (self.name, self.breed))
                self.id = c.lastrowid
        else:
            with sqlite3.connect(self.db) as conn:
                c = conn.cursor()
                c.execute('''UPDATE dogs SET name=?, breed=? WHERE id=?''', (self.name, self.breed, self.id))

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        id, name, breed = data
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        with sqlite3.connect(cls.db) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM dogs''')
            return [cls.new_from_db(row) for row in c.fetchall()]

    @classmethod
    def find_by_name(cls, name):
        with sqlite3.connect(cls.db) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM dogs WHERE name=?''', (name,))
            data = c.fetchone()
            if data:
                return cls.new_from_db(data)
            else:
                return None

    @classmethod
    def find_by_id(cls, id):
        with sqlite3.connect(cls.db) as conn:
            c = conn.cursor()
            c.execute('''SELECT * FROM dogs WHERE id=?''', (id,))
            data = c.fetchone()
            if data:
                return cls.new_from_db(data)
            else:
                return None

    def update(self):
        if self.id:
            with sqlite3.connect(self.db) as conn:
                c = conn.cursor()
                c.execute('''UPDATE dogs SET name=?, breed=? WHERE id=?''', (self.name, self.breed, self.id))

    
    
