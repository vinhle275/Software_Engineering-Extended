# event_manager.py
# Feature: Create Event – Smart Event Reminder System (SERS)
# Version: 1.0

from datetime import datetime
from typing import Optional
import uuid

# Data model 
class Event:
    """Represents a single user event in SERS."""
    def __init__(
        self,
        title: str,
        event_date: str,          # format: YYYY-MM-DD
        event_time: str,          # format: HH:MM
        description: str = "",
        location: Optional[str] = None,
        reminder_minutes: int = 30
    ):
        self.event_id: str = str(uuid.uuid4())[:8]
        self.title = title
        self.event_date = event_date
        self.event_time = event_time
        self.description = description
        self.location = location
        self.reminder_minutes = reminder_minutes
        self.status: str = "Scheduled"  # Created -> Scheduled -> Notified -> Completed
        self.created_at: str = datetime.now().strftime("%Y-%m-%d %H:%M")

    def to_dict(self) -> dict:
        """Serialize event to dictionary (e.g., for JSON storage)."""
        return {
            "event_id": self.event_id,
            "title": self.title,
            "event_date": self.event_date,
            "event_time": self.event_time,
            "description": self.description,
            "location": self.location,
            "reminder_minutes": self.reminder_minutes,
            "status": self.status,
        }

# Event Manager
class EventManager:
    """Manages creation, update, deletion, and retrieval of events."""
    def __init__(self):
        self._events: dict[str, Event] = {}  # event_id → Event

    # Validation helpers
    def _validate_title(self, title: str) -> None:
        if not title or not title.strip():
            raise ValueError("Event title cannot be empty.")
        if len(title) > 100:
            raise ValueError("Title must be 100 characters or fewer.")

    def _validate_datetime(self, date_str: str, time_str: str) -> None:
        try:
            event_dt = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid date/time format. Use YYYY-MM-DD and HH:MM.")
        if event_dt <= datetime.now():
            raise ValueError("Event must be scheduled in the future.")

    def _validate_reminder(self, minutes: int) -> None:
        if minutes < 0:
            raise ValueError("Reminder offset cannot be negative.")

    # CRUD operations 
    def create_event(
        self,
        title: str,
        event_date: str,
        event_time: str,
        description: str = "",
        location: Optional[str] = None,
        reminder_minutes: int = 30
    ) -> Event:
        """Validate inputs and create a new event."""
        self._validate_title(title)
        self._validate_datetime(event_date, event_time)
        self._validate_reminder(reminder_minutes)
        new_event = Event(
            title=title.strip(),
            event_date=event_date,
            event_time=event_time,
            description=description,
            location=location,
            reminder_minutes=reminder_minutes,
        )
        self._events[new_event.event_id] = new_event
        print(f"[SERS] Event '{new_event.title}' created (ID: {new_event.event_id}).")
        return new_event

    def get_event(self, event_id: str) -> Event:
        """Retrieve an event by ID; raise if not found."""
        if event_id not in self._events:
            raise KeyError(f"No event found with ID '{event_id}'.")
        return self._events[event_id]

    def delete_event(self, event_id: str) -> bool:
        """Remove an event; returns True on success."""
        event = self.get_event(event_id)       # raises if not found
        del self._events[event_id]
        print(f"[SERS] Event '{event.title}' deleted.")
        return True

    def list_events(self) -> list[Event]:
        """Return all events sorted by date/time ascending."""
        return sorted(
            self._events.values(),
            key=lambda e: (e.event_date, e.event_time)
        )

# Usage example (mock run)
if __name__ == "__main__":
    manager = EventManager()
    try:
        e = manager.create_event(
            title="Team Stand-up",
            event_date="2026-05-10",
            event_time="09:00",
            description="Daily sync meeting",
            location="Room 3B",
            reminder_minutes=15
        )
        print(e.to_dict())
    except ValueError as err:
        print(f"[ERROR] {err}")
