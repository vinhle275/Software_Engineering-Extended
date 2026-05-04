# test_event_manager.py
import unittest
from event_manager import EventManager

class TestCreateEvent(unittest.TestCase):

    def setUp(self):
        self.manager = EventManager()

    # T1 – valid event creation
    def test_create_valid_event(self):
        event = self.manager.create_event(
            title="Team Meeting", event_date="2026-05-10", event_time="09:00"
        )
        self.assertEqual(event.title, "Team Meeting")
        self.assertEqual(event.status, "Scheduled")

    # T2 – empty title raises ValueError
    def test_empty_title_raises_error(self):
        with self.assertRaises(ValueError) as ctx:
            self.manager.create_event(title="", event_date="2026-05-10", event_time="09:00")
        self.assertIn("cannot be empty", str(ctx.exception))

if __name__ == "__main__":
    unittest.main()
