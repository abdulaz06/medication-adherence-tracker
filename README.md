# Medication & Supplement Adherence Tracker

A full-stack mobile application for tracking daily medication and supplement intake, analyzing adherence over time, and visualizing trends. Built with **Flutter** (frontend) and **FastAPI** (backend).

> **Disclaimer:** This application is for educational and research purposes only and does **not** provide medical advice, diagnosis, or treatment recommendations.

---

## Screenshots

| Today View | Items | Stats | History |
|:---:|:---:|:---:|:---:|
| Daily schedule with take/skip | Manage medications | Adherence analytics | Browse past days |

---

## Features

### Core Tracking
- Add medications and supplements with custom schedules
- Flexible scheduling via day-of-week bitmask (e.g., weekdays only, weekends, custom)
- Support for multiple doses per day
- Mark each dose as **Taken** or **Skipped** with optional skip reasons
- Duplicate prevention (can't log the same dose twice)

### Daily View
- "Today" screen showing all scheduled items for the current day
- Real-time progress bar (X of Y doses completed)
- Color-coded medication vs supplement indicators

### Analytics & Streaks
- 7-day, 14-day, and 30-day adherence percentages
- Per-item adherence breakdown (taken / skipped / missed)
- Current streak and longest streak tracking
- Visual progress rings and bar charts

### History
- Browse any past day's schedule and completion status
- Date picker navigation

### Authentication
- JWT-based auth (register + login)
- Bcrypt password hashing
- Bearer token for API requests

### User Experience
- Material 3 design with light/dark mode
- Responsive layout for mobile and web
- Pull-to-refresh on all data screens
- Profile and settings screen

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Flutter 3.x (Dart), Provider, Material 3 |
| **Backend** | FastAPI (Python), Pydantic v2 |
| **ORM** | SQLAlchemy 2.0 (mapped typing) |
| **Database** | SQLite (dev), PostgreSQL-compatible |
| **Auth** | JWT (python-jose) + bcrypt |
| **API Docs** | Swagger UI auto-generated at `/docs` |

---

## Architecture

```
Flutter App (Mobile / Web)
         ↓ HTTP / REST
FastAPI Backend
         ↓ SQLAlchemy ORM
SQLite Database (dev)
```

### Data Model

```
users
├── id, email, password_hash
│
├── items (medications & supplements)
│   ├── id, user_id (FK), name, type
│   ├── doses_per_day, schedule_days (bitmask)
│   ├── notes, active
│   │
│   └── dose_logs
│       ├── id, item_id (FK), user_id (FK)
│       ├── scheduled_date, dose_index
│       ├── status (taken/skipped), timestamp
│       └── skip_reason
```

**Schedule Bitmask Encoding:**
| Day | Bit Value |
|-----|-----------|
| Mon | 1 |
| Tue | 2 |
| Wed | 4 |
| Thu | 8 |
| Fri | 16 |
| Sat | 32 |
| Sun | 64 |

`127` = every day, `62` = Mon–Fri, `96` = weekends only

---

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Create account |
| POST | `/auth/login` | Get JWT token |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Current user profile |
| GET | `/users/{id}` | Get user by ID |

### Items
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/items/` | Create item |
| GET | `/items/by-user/{user_id}` | List user's items |
| GET | `/items/{item_id}` | Get single item |
| PATCH | `/items/{item_id}` | Update item |
| DELETE | `/items/{item_id}` | Delete item |

### Dose Logs
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/logs/items/{item_id}` | Log a dose |
| GET | `/logs/by-user/{user_id}` | List logs (with date filters) |
| PATCH | `/logs/{log_id}` | Update log status |
| DELETE | `/logs/{log_id}` | Remove a log |

### Schedule & Stats
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/logs/schedule/{user_id}` | Today's schedule with completion |
| GET | `/logs/stats/{user_id}` | Adherence stats & streaks |

### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/db-check` | Database connectivity |

---

## Getting Started

### Prerequisites
- Python 3.11+
- Flutter 3.x
- Git

### Backend Setup

```bash
cd backend

# Create virtual environment (recommended)
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`
Swagger docs at `http://127.0.0.1:8000/docs`

> **Important:** Always run uvicorn from the `backend/` directory, not from subfolders.

### Frontend Setup

```bash
cd frontend

# Install dependencies
flutter pub get

# Run in Chrome (web)
flutter run -d chrome

# Run on connected Android device
flutter run
```

> **Note:** The backend must be running for the frontend to work.

---

## Project Structure

```
medication-adherence-tracker/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── auth.py              # Password hashing + JWT
│   │   ├── dependencies.py      # Auth dependency injection
│   │   ├── db/
│   │   │   ├── session.py       # Engine, session, get_db
│   │   │   └── utils.py         # create_tables, db_check
│   │   ├── models/
│   │   │   ├── user.py          # User model
│   │   │   ├── item.py          # Item model
│   │   │   └── dose_log.py      # DoseLog model
│   │   ├── schemas/
│   │   │   ├── user.py          # User schemas
│   │   │   ├── item.py          # Item schemas
│   │   │   ├── auth.py          # Auth schemas
│   │   │   └── dose_log.py      # Log + schedule + stats schemas
│   │   └── routers/
│   │       ├── auth.py          # Register + login
│   │       ├── users.py         # User endpoints
│   │       ├── items.py         # Item CRUD
│   │       └── dose_logs.py     # Logging + schedule + stats
│   └── requirements.txt
├── frontend/
│   ├── lib/
│   │   ├── main.dart            # App entry point
│   │   ├── models/models.dart   # Data models
│   │   ├── services/
│   │   │   ├── api_service.dart # HTTP client
│   │   │   └── app_state.dart   # Provider state
│   │   └── screens/
│   │       ├── login_screen.dart
│   │       ├── home_screen.dart
│   │       ├── today_screen.dart
│   │       ├── items_screen.dart
│   │       ├── history_screen.dart
│   │       └── stats_screen.dart
│   └── pubspec.yaml
└── docs/
    └── PROJECT_SPEC.md
```

---

## Development Notes

### Known Environment Considerations
- **Windows:** Use PowerShell; activate venv with `.venv\Scripts\Activate.ps1`
- **macOS:** Use zsh; activate venv with `source .venv/bin/activate`
- **email-validator:** Required by Pydantic EmailStr — installed via `pydantic[email]`
- **SQLite FK enforcement:** Enabled via SQLAlchemy event listener (`PRAGMA foreign_keys=ON`)
- **Flutter Developer Mode:** Required on Windows for symlinks — enable in Settings → Developer

### Commit Conventions
- `feat:` — new functionality
- `fix:` — bug correction
- `refactor:` — structural cleanup
- `docs:` — documentation changes

---

## Planned v2 Features
- SMS/WhatsApp dose reminders (Twilio integration)
- Push notifications (local + remote)
- CSV/PDF export
- Offline-first support
- Advanced analytics and trend charts

---

## Authors
Built as a collaborative project by two CS majors using pair programming (driver/navigator model).

---

## License
See [LICENSE](LICENSE) for details.
