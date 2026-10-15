
"""Manage event bookings, guests, reports, and saved data."""

import json
import secrets
from datetime import date
from pathlib import Path

events = {}


def create_event(event_name, venue, capacity=50, guests=None):
    """Create an event with an independent guest list."""
    if guests is None:
        guests = []
    events[event_name] = {
        "venue": venue,
        "capacity": capacity,
        "guests": list(guests)
    }
    return events[event_name]


def register_guest(event_name, guest):
    """Register a guest when the event has available seats."""
    event = events.get(event_name)
    if event is None:
        print("No such event:", event_name)
        return False
    if len(event["guests"]) >= event["capacity"]:
        print(event_name, "is full, cannot add", guest)
        return False
    event["guests"].append(guest)
    return True


def seats_left(event_name):
    """Return the number of seats remaining."""
    event = events[event_name]
    return event["capacity"] - len(event["guests"])


def event_status(event_date):
    """Return the status of an event based on its date."""
    if event_date >= date.today():
        return "Upcoming"
    return "Completed"


def guest_report(event_name, sort_order):
    """Return guest names sorted in the requested order."""
    names = sorted(
        events[event_name]["guests"],
        reverse=sort_order == "desc"
    )
    return ", ".join(names)


def save_events(file_name="events.json"):
    """Save event data to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(events, file)


def load_events(file_name="events.json"):
    """Load saved event data from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def print_badges(event_name):
    """Display a badge file without running shell commands."""
    badge_file = Path("badges_" + event_name + ".txt")
    if not badge_file.is_file():
        print("Badge file not found:", badge_file)
        return
    print(badge_file.read_text(encoding="utf-8"))


def main():
    """Demonstrate event creation, registration, and storage."""
    create_event("Tech Meetup", "Hall A", 3)
    create_event("Alumni Dinner", "Rooftop", 2)
    register_guest("Tech Meetup", "Asha")
    register_guest("Tech Meetup", "Ravi")
    register_guest("Alumni Dinner", "Meena")
    register_guest("Workshop", "Kiran")
    left = seats_left("Tech Meetup")
    print("Seats left at Tech Meetup:", left)
    print("Seats left at Alumni Dinner:", seats_left("Alumni Dinner"))
    print("Tech Meetup guests:", guest_report("Tech Meetup", "name"))
    print("Tech Meetup is", event_status(date(2099, 1, 15)))
    print("Alumni Dinner is", event_status(date(2020, 5, 1)))
    winner = secrets.choice(events["Tech Meetup"]["guests"])
    print("Lucky draw winner:", winner)
    save_events()
    restored = load_events()
    print("Events restored from file:", len(restored))
    print("Venues:", [event["venue"] for event in restored.values()])


if __name__ == "__main__":
    main()
