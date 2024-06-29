# SAF (Servei d'Activitat Fisica) UAB availability checker
This is a tool to check my gym's availability from my terminal. Currently it is possible to check today's and tomorrow's availability.

## Time Slot States
A time slot can be on three different states:

- Not Available: Past times
- Full: Currently full, but still not past
- Available

## Future Features
On the near future I plan on adding new functionality, such as the ability to log in and book available time slots.

## Installation

```bash
git clone https://github.com/antthegreekgod/SAF-availability.git
cd SAF-availability
pip3 install -r requirements.txt
```

## Usage

```python
python3 saf.py
```
