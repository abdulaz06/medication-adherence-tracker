Medication & Supplement Adherence Tracker — 14-Day MVP Project Spec

1. Project Overview
This project is a Medication & Supplement Adherence Tracker designed as an educational / research prototype.
 The goal is to build a clean, functional mobile application that allows users to track daily medication and supplement intake, analyze adherence over time, and visualize trends.
This project is being developed by two CS majors as joint primary owners, using pair programming and shared design ownership.
The project is intentionally scoped as a minimum viable product (MVP) to be completed in 14 days, with a focus on:
clean architecture


strong data modeling


real backend + database integration


Flutter-based mobile development


Disclaimer:
 This application is for educational and research purposes only and does not provide medical advice, recommendations, or diagnosis.




2. Goals & Motivation
Primary goals
Demonstrate proficiency in:


Object-Oriented Programming (OOP)


Full-stack software development


Database design and usage


Flutter mobile development


Build a recovery-adjacent health tracking app aligned with academic research needs


Produce an internship-ready project with real engineering depth


Non-goals (explicitly out of scope)
Medical recommendations or dosing logic


Clinical decision-making


AI/ML-based health insights


Notifications or reminders (planned for v2)


Offline-first synchronization (planned for v2)







3. MVP Feature Scope
Included in v1 (locked)
User profile


Add medication or supplement


Schedule:


daily


custom days (Mon–Sun)


Doses per day


“Today” view showing scheduled doses


Mark dose as Taken or Skipped


Optional skip reason


History view (by date)


Adherence analytics:


7-day adherence %


30-day adherence %


per-item adherence


Streak tracking:


current streak


longest streak


PostgreSQL-backed persistence


Flutter UI with clean navigation


README + screenshots


Explicitly excluded from v1
Push notifications


Offline caching


AI features


PDF/advanced export


UI animations or visual polish beyond clarity



4. Tech Stack
Frontend
Flutter (Dart)


State management: Provider or Riverpod (one chosen and locked)


Backend
FastAPI (Python)


RESTful API


Database
PostgreSQL


Tooling
GitHub (single shared repository)


Pair programming (driver/navigator model)



5. Architecture Overview
High-level flow:
Flutter App
   ↓ REST API
FastAPI Backend
   ↓ ORM
PostgreSQL Database

Flutter handles UI, state, and API interaction


FastAPI handles authentication, business logic, and analytics


PostgreSQL stores all structured data



6. Data Model (Core Design)
users
id


email


hashed_password


created_at


items (medications & supplements)
id


user_id (FK → users)


name


type (medication / supplement)


doses_per_day


schedule_days (array or bitmask)


notes


active (boolean)


dose_logs
id


item_id (FK → items)


scheduled_date


status (taken / skipped)


timestamp


skip_reason (nullable)


Key derived metrics
Adherence percentage (taken ÷ scheduled)


Current streak


Longest streak


Missed dose count



7. Screen Flow (Flutter)
Login / Profile


user info


baseline setup


Today


list of scheduled doses


mark Taken / Skipped


Add / Edit Item


name


type


schedule


doses per day


History


daily logs


taken vs skipped


Stats


adherence %


streaks


per-item trends



8. Pair Programming & Ownership Model
Both developers are joint primary owners


All major components are:


jointly designed


pair-programmed


reviewed together


Driver / Navigator roles rotate every 30–60 minutes


A weekly “decision driver” resolves tie-breakers (rotated weekly)


Both developers can independently:


explain architecture


explain DB schema


walk through API flows


describe tradeoffs and future improvements



9. 14-Day Timeline (Locked)
Days 1–2
Finalize scope (this document)


Schema design


Screen flow


Repo setup


Days 3–6
PostgreSQL schema


FastAPI project structure


CRUD endpoints


Auth (basic)


Days 7–10
Flutter screens


API integration


Today view + logging flow


Days 11–12
Adherence analytics


Streak logic


Stats screen


Days 13–14
Cleanup


Error handling


README finalization


Screenshots / demo


Rule: Timeline does not move. Scope moves if needed.

10. Planned v2 Extensions (Not Implemented)
Notifications/reminders


Offline-first support


CSV/PDF export


AI-assisted insights


Advanced analytics



11. Success Criteria
The project is considered successful if:
The app works end-to-end


Data persists correctly


Analytics are accurate


Both developers can fully explain the system


The project is demo-ready by end of January



