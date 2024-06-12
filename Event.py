"""
Описывает некоторе "событие" - промежуток времени с присвоенными характеристиками
У события должно быть описание, название и список участников
Событие может быть единожды созданым
Или периодическим (каждый день/месяц/год/неделю)

Каждый пользователь ивента имеет свою "роль"
организатор умеет изменять названия, список участников, описание, а так же может удалить событие
участник может покинуть событие

запрос на хранение в json
Уметь создавать из json и записывать в него

Иметь покрытие тестами
Комментарии на нетривиальных методах и в целом документация
"""

import json
import unittest
from datetime import datetime


class Event:
    def __init__(self, name, description, organizer, participants, start_time, is_recurring=False,
                 recurrence_type=None):
        self.name = name
        self.description = description
        self.organizer = organizer
        self.participants = participants
        self.start_time = start_time
        self.is_recurring = is_recurring
        self.recurrence_type = recurrence_type
        self.creation_time = datetime.now()

    def add_participant(self, participant):
        self.participants.append(participant)

    def remove_participant(self, participant):
        if participant in self.participants:
            self.participants.remove(participant)

    def update_event(self, name=None, description=None, participants=None):
        if self.organizer == self.organizer:
            if name:
                self.name = name
            if description:
                self.description = description
            if participants:
                self.participants = participants

    def delete_event(self):
        if self.organizer == self.organizer:
            pass

    def to_json(self):
        return json.dumps(self.__dict__)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)


class TestEvent(unittest.TestCase):
    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.organizer = None

    def setUp(self):
        self.orgainizer = 'Organizer1'
        self.participant1 = 'Participant1'
        self.participant2 = 'Participant2'
        self.event_name = 'EventName'
        self.event_description = 'EventDescription'
        self.start_time = datetime.now()
        self.recurrence_type = 'daily'

    def test_event_creation(self):
        event = Event(self.event_name, self.event_description, self.orgainizer, [self.participant1], self.start_time)
        self.assertEqual(event.name, self.event_name)
        self.assertEqual(event.description, self.event_description)
        self.assertEqual(event.organizer, self.orgainizer)
        self.assertEqual(event.participants, [self.participant1])
        self.assertEqual(event.start_time, self.start_time)

    def test_add_participant(self):
        event = Event(self.event_name, self.event_description, self.orgainizer, [self.participant1], self.start_time)
        event.add_participant(self.participant2)
        self.assertIn(self.participant2, event.participants)

    def test_remove_participant(self):
        event = Event(self.event_name, self.event_description, self.organizer, [self.participant1, self.participant2],
                      self.start_time)
        event.remove_participant(self.participant2)
        self.assertNotIn(self.participant2, event.participants)

    def test_update_event(self):
        event = Event(self.event_name, self.event_description, self.organizer, [self.participant1, self.participant2],
                      self.start_time)
        new_name = 'NewEventName'
        new_description = 'NewDescrip'
        new_participants = [self.participant1, self.participant2]
        event.update_event(name=new_name, description=new_description, participants=new_participants)
        self.assertEqual(event.name, new_name)
        self.assertEqual(event.description, new_description)
        self.assertEqual(event.participants, new_participants)

    def test_delete_event(self):
        event = Event(self.event_name, self.event_description, self.organizer, [self.participant1, self.participant2],
                      self.start_time)
        event.delete_event()

    def test_to_json_and_from_json(self):
        event = Event(self.event_name, self.event_description, self.organizer, [self.participant1, self.participant2],
                      self.start_time)
        json_str = event.to_json()
        new_event = Event.from_json(json_str)
        self.assertEqual(new_event.name, event.name)
        self.assertEqual(new_event.description, event.description)
        self.assertEqual(new_event.organizer, event.organizer)
        self.assertEqual(new_event.participants, event.participants)
        self.assertEqual(new_event.start_time, event.start_time)
