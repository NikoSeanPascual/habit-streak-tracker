# Habit Streak Tracker (CustomTkinter)

A desktop **Habit Streak Tracker** built with **Python** and **CustomTkinter** that helps users build consistency by tracking daily habit completion, calculating streaks, and visualizing progress through a heatmap-style calendar.

The application is fully local, lightweight, and focuses on **correct streak logic**, **clean separation of concerns**, and a **terminal-inspired UI aesthetic**.

---

## Features

### Habit Management
- Create and delete habits
- Prevents duplicate or empty habit names
- Each habit stores its own start date and history

### Daily Check-In System
- Mark habits as completed or pending for **today**
- Only one completion state per habit per day
- Toggle today’s completion at any time

### Streak Tracking
- **Current Streak**: Consecutive completed days ending today
- **Longest Streak**: Maximum consecutive completion run
- Automatic streak reset when a day is missed
- All streaks are **calculated from history**, not stored counters

### Progress Visualization
- 60-day **heatmap calendar**
- Color-coded:
  - Completed days
  - Missed days
  - Today highlighted
- Immediate visual feedback on consistency

### Statistics Dashboard
- Current streak
- Longest streak
- Completion rate (%)
- Today’s completion status
- Warning message if streak was broken yesterday

### Local Data Persistence
- All data stored in a human-readable **JSON file**
- No accounts, no cloud, no external dependencies
