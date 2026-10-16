# Pinterest-Scheduler

A lightweight CLI app to schedule Pinterest pins and generate calendar events.

## Features
- Accept Pinterest pin URLs
- Schedule pins for specific days/times
- Output a Google Calendar event link
- Output a generic `.ics` event payload for other calendars

## Usage

Schedule a pin and get a Google Calendar link:

```bash
python app.py schedule \
  --pin-url "https://www.pinterest.com/pin/12345" \
  --when "2026-11-01T10:00:00+00:00" \
  --title "Morning Pin"
```

Schedule a pin and get an ICS event:

```bash
python app.py schedule \
  --pin-url "https://www.pinterest.com/pin/12345" \
  --when "2026-11-01T10:00:00+00:00" \
  --calendar ics
```

List scheduled pins:

```bash
python app.py list
```