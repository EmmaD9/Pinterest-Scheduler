import tempfile
import unittest
from pathlib import Path

from app import PinterestScheduler


class PinterestSchedulerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.storage_path = Path(self.temp_dir.name) / "pins.json"
        self.scheduler = PinterestScheduler(storage_file=self.storage_path)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_schedule_pin_accepts_pinterest_url(self) -> None:
        pin = self.scheduler.schedule_pin(
            pin_url="https://www.pinterest.com/pin/12345",
            scheduled_for="2026-11-01T10:00:00+00:00",
            title="Morning post",
        )
        self.assertEqual(pin.title, "Morning post")
        self.assertEqual(len(self.scheduler.list_scheduled_pins()), 1)

    def test_schedule_pin_rejects_non_pinterest_url(self) -> None:
        with self.assertRaises(ValueError):
            self.scheduler.schedule_pin(
                pin_url="https://example.com/pin/12345",
                scheduled_for="2026-11-01T10:00:00+00:00",
            )

    def test_google_calendar_link_contains_event_data(self) -> None:
        pin = self.scheduler.schedule_pin(
            pin_url="https://www.pinterest.com/pin/12345",
            scheduled_for="2026-11-01T10:00:00+00:00",
            title="Launch Pin",
        )
        link = self.scheduler.google_calendar_link(pin)
        self.assertIn("calendar/render", link)
        self.assertIn("text=Launch+Pin", link)
        self.assertIn("dates=20261101T100000Z%2F20261101T103000Z", link)

    def test_ics_event_contains_calendar_fields(self) -> None:
        pin = self.scheduler.schedule_pin(
            pin_url="https://www.pinterest.com/pin/12345",
            scheduled_for="2026-11-01T10:00:00+00:00",
            title="Launch Pin",
        )
        ics = self.scheduler.ics_event(pin)
        self.assertIn("BEGIN:VCALENDAR", ics)
        self.assertIn("DTSTART:20261101T100000Z", ics)
        self.assertIn("SUMMARY:Launch Pin", ics)


if __name__ == "__main__":
    unittest.main()
