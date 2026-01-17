# Medication & Supplement Adherence Tracker

A mobile application for tracking daily medication and supplement adherence, built as an educational and research-oriented prototype.

This project focuses on clean software architecture, structured data modeling, and end-to-end full-stack development using a modern mobile + backend stack.

> **Disclaimer:** This application is for educational and research purposes only and does **not** provide medical advice, diagnosis, or treatment recommendations.

---

## Features (MVP)

- User account and basic profile
- Add medications or supplements
- Flexible schedules:
  - Daily
  - Custom days of the week
- Support for multiple doses per day
- Daily **Today** view showing scheduled doses
- Mark doses as **Taken** or **Skipped**
- Optional skip reasons
- History view of logged doses by date
- Adherence analytics:
  - 7-day adherence percentage
  - 30-day adherence percentage
  - Per-item adherence
- Streak tracking:
  - Current streak
  - Longest streak
- Persistent backend with database storage

---

## Tech Stack

### Frontend
- Flutter (Dart)

### Backend
- FastAPI (Python)
- RESTful API

### Database
- PostgreSQL

### Tooling
- GitHub
- Visual Studio Code

---

## Architecture Overview

```text
Flutter Mobile App
        ↓
   FastAPI REST API
        ↓
 PostgreSQL Database