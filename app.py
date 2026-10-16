from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List
from urllib.parse import quote, urlencode, urlparse
from uuid import uuid4


STORAGE_FILE = Path.home() / ".pinterest_scheduler.json"


@dataclass
class ScheduledPin:
    id: str
    pin_url: str
    title: str
    scheduled_for: str
    duration_minutes: int
    timezone_name: str

    @property
    def starts_at(self) -> datetime:
        return datetime.fromisoformat(self.scheduled_for)

    @property
    def ends_at(self) -> datetime:
        return self.starts_at + timedelta(minutes=self.duration_minutes)


class PinterestScheduler:
    def __init__(self, storage_file: Path = STORAGE_FILE):
        self.storage_file = storage_file
        self._scheduled_pins: List[ScheduledPin] = self._load()

    def schedule_pin(
        self,
        pin_url: str,
        scheduled_for: str,
        title: str | None = None,
        duration_minutes: int = 30,
        timezone_name: str = "UTC",
    ) -> ScheduledPin:
        parsed_pin = urlparse(pin_url)
        if "pinterest." not in parsed_pin.netloc:
            raise ValueError("pin_url must be a valid Pinterest URL")

        event_start = datetime.fromisoformat(scheduled_for)
        if event_start.tzinfo is None:
            event_start = event_start.replace(tzinfo=timezone.utc)

        scheduled = ScheduledPin(
            id=str(uuid4()),
            pin_url=pin_url,
            title=title or "Scheduled Pinterest Pin",
            scheduled_for=event_start.isoformat(),
            duration_minutes=duration_minutes,
            timezone_name=timezone_name,
        )
        self._scheduled_pins.append(scheduled)
        self._save()
        return scheduled

    def list_scheduled_pins(self) -> List[ScheduledPin]:
        return list(self._scheduled_pins)

    @staticmethod
    def google_calendar_link(pin: ScheduledPin) -> str:
        start = pin.starts_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        end = pin.ends_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        params = {
            "action": "TEMPLATE",
            "text": pin.title,
            "details": f"Pinterest pin to publish: {pin.pin_url}",
            "dates": f"{start}/{end}",
            "ctz": pin.timezone_name,
        }
        return f"https://calendar.google.com/calendar/render?{urlencode(params)}"

    @staticmethod
    def ics_event(pin: ScheduledPin) -> str:
        start = pin.starts_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        end = pin.ends_at.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        return (
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "BEGIN:VEVENT\n"
            f"UID:{pin.id}\n"
            f"DTSTAMP:{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}\n"
            f"DTSTART:{start}\n"
            f"DTEND:{end}\n"
            f"SUMMARY:{pin.title}\n"
            f"DESCRIPTION:Pinterest pin to publish: {quote(pin.pin_url, safe=':/')}\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n"
        )

    def _load(self) -> List[ScheduledPin]:
        if not self.storage_file.exists():
            return []
        data = json.loads(self.storage_file.read_text(encoding="utf-8"))
        return [ScheduledPin(**item) for item in data]

    def _save(self) -> None:
        payload = [asdict(item) for item in self._scheduled_pins]
        self.storage_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Schedule Pinterest pins.")
    subcommands = parser.add_subparsers(dest="command", required=True)

    schedule = subcommands.add_parser("schedule", help="Schedule a Pinterest pin")
    schedule.add_argument("--pin-url", required=True, help="Pinterest URL to schedule")
    schedule.add_argument(
        "--when",
        required=True,
        help="When to schedule (ISO 8601, e.g. 2026-11-01T10:00:00+00:00)",
    )
    schedule.add_argument("--title", default="Scheduled Pinterest Pin")
    schedule.add_argument("--duration-minutes", type=int, default=30)
    schedule.add_argument("--timezone", default="UTC")
    schedule.add_argument(
        "--calendar",
        choices=("google", "ics"),
        default="google",
        help="Calendar output type",
    )

    subcommands.add_parser("list", help="List scheduled Pinterest pins")
    return parser


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    scheduler = PinterestScheduler()

    if args.command == "schedule":
        pin = scheduler.schedule_pin(
            pin_url=args.pin_url,
            scheduled_for=args.when,
            title=args.title,
            duration_minutes=args.duration_minutes,
            timezone_name=args.timezone,
        )
        if args.calendar == "google":
            print(PinterestScheduler.google_calendar_link(pin))
        else:
            print(PinterestScheduler.ics_event(pin))
    elif args.command == "list":
        for pin in scheduler.list_scheduled_pins():
            print(f"{pin.id} | {pin.scheduled_for} | {pin.title} | {pin.pin_url}")


if __name__ == "__main__":
    main()
