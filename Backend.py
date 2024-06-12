"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.
"""
"""
Сущность, отвечающая за храние и предоставление данных
Оно хранит пользователей, календари и события.
Хранение в том числе означает сохранение между сессиями в csv файлах
(пароли пользователей хранятся как hash)

Должен быть статическим или Синглтоном

*) Нужно хранить для каждого пользователя все события которые с нима произошли но ещё не были обработаны.

"""

import tempfile
import unittest
import csv
import hashlib
import os


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


class Backend:
    _instance = None

    def __init__(self):
        self._users = None
        self.users = None
        self._events = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Backend, cls).__new__(cls)
            cls._instance._users = {}
            cls._instance._events = {}
            cls._instance._users_file = "users.csv"
            cls._instance._events_file = "events.csv"
            cls._instance.load_users()
            cls._instance.load_events()
        return cls._instance

    def add_user(self, username, password):
        hashed_password = hash_password(password)
        if username not in self._users:
            self._users[username] = {"password": hashed_password}
            self.save_users()

    def verify_user(self, username, password):
        hashed_password = hash_password(password)
        return username in self._users and self._users[username]["password"] == hashed_password

    def add_event(self, username, event):
        if username in self._users:
            if username not in self._events:
                self._events[username] = []
            self._events[username].append(event)
            self.save_events()

    def get_pending_events(self, username):
        return self._events.get(username, [])

    def clear_events(self, username):
        if username in self._events:
            del self._events[username]
            self.save_events()

    def load_users(self):
        if os.path.exists(self._users_file):
            with open(self._users_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self._users = {row["username"]: {"password": row["password"]} for row in reader}

    def save_users(self):
        with open(self._users_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["username", "password"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for username, data in self._users.items():
                writer.writerow({"username": username, "password": data["password"]})

    def load_events(self):
        if os.path.exists(self._events_file):
            with open(self._events_file, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self._events = {row["username"]: eval(row["events"]) for row in reader}

    def save_events(self):
        with open(self._events_file, mode="w", newline="", encoding="utf-8") as file:
            fieldnames = ["username", "events"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for username, events in self._events.items():
                writer.writerow({"username": username, "events": str(events)})


class TestBackend(unittest.TestCase):
    def setUp(self):
        self.backend = Backend()
        self.temp_dir = tempfile.mkdtemp()
        self.backend._users_file = os.path.join(self.temp_dir, 'users.csv')
        self.backend._events_file = os.path.join(self.temp_dir, 'events.csv')

    def test_add_user(self):
        self.backend.add_user("test_user", "password123")
        self.assertTrue('test_user' in self.backend.users)
        self.assertNotEqual(self.backend._users['test_user']['password'], 'password123')

    def test_add_event(self):
        self.backend.add_user('test_user', 'password123')
        event = {'type': 'notification', 'content': 'Test event'}
        self.backend.add_event('test_user', event)
        self.assertTrue("test_user" in self.backend._events)
        self.assertEqual(len(self.backend._events['test_user']), 1)
        self.assertEqual(self.backend._events['test_user'][0], event)

    def test_clear_events(self):
        self.backend.add_user("test_user", "password123")
        event = {'type': 'notification', 'content': 'Test event'}
        self.backend.add_event("test_user", event)

        self.backend.clear_events('test_user')
        self.assertTrue('test_user' not in self.backend._events)
