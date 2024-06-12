"""
Класс календаря - хранит события.
он умеет искать все события из промежутка (в том числе повторяющиеся)
он умеет добавлять/удалять события.
У каждого календаря ровно один пользователь.
"""


from Event import Event
from datetime import datetime
import unittest

class Calendar:
    def __init__(self, user):
        self.user = user
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def remove_event(self, event):
        if event in self.events:
            self.events.remove(event)

    def search_events_in_interval(self, start_time, end_time):
        result = []
        for event in self.events:
            if event.start_time >= start_time and event.start_time <= end_time:
                result.append(event)
        return result


class TestCalendar(unittest.TestCase):

    def setUp(self):
        self.calendar = Calendar(user="test_user")

    def test_add_event(self):
        event = Event('Test Event', datetime(2024, 2, 5, 12))
        self.calendar.add_event(event)
        self.assertIn(event, self.calendar.events)

    def test_remove_event(self):
        event = Event('Test Event', datetime(2024, 2, 5, 12))
        self.calendar.add_event(event)
        self.calendar.remove_event(event)
        self.assertNotIn(event, self.calendar.events)

    def test_search_events_in_interval(self):
        event1 = Event('Event1', datetime(2024, 2, 5, 12))
        event2 = Event('Event2', datetime(2024, 2, 7, 12))
        event3 = Event('Event3', datetime(2024, 2, 8, 12))

        self.calendar.add_event(event1)
        self.calendar.add_event(event2)
        self.calendar.add_event(event3)

        start_time = datetime(2024, 2, 5, 0)
        end_time = datetime(2024, 2, 7, 23)

        result = self.calendar.search_events_in_interval(start_time, end_time)

        self.assertIn(event1, result)
        self.assertIn(event2, result)
        self.assertNotIn(event3, result)

if __name__ == "__main__":
    unittest.main()
