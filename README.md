# 🐍 Python Projects

A collection of Python capstone projects built while learning Python fundamentals, web scraping, API integration, and web development.

---

## Projects

### 🐢 Day 23 — Crossy Road (Turtle Graphics)
A **Frogger / Crossy Road clone** built with Python's `turtle` module. The player navigates a turtle across a busy road, dodging randomly spawning cars that speed up with each successful crossing.

**Tech:** Python, Turtle Graphics

---

### ✈️ Day 39–40 — Flight Deal Finder
An automated **flight deal tracker** that searches for the cheapest flights from Singapore to a list of destinations using the Amadeus API. When a price drops below a recorded threshold, it emails all registered users via SMTP. Destination data and user emails are managed through a Google Sheet (Sheety API).

**Tech:** Python, Amadeus API, Sheety API, SMTP, `dotenv`

---

### 🏠 Day 53 — Rent Scraping
A **web scraping bot** that extracts rental property listings (prices, addresses, links) from a Zillow clone page using BeautifulSoup, then automatically fills out a Google Form with the scraped data using Selenium.

**Tech:** Python, BeautifulSoup, Selenium, Requests

---

### ✍️ Day 69 — Blog with Users
A full-featured **multi-user blog** built with Flask. Supports user registration/login (with hashed passwords), an admin-only post management system, a CKEditor-powered rich text editor, a relational comment system, and Gravatar integration.

**Tech:** Python, Flask, SQLAlchemy, Flask-Login, WTForms, Bootstrap 5, CKEditor

---

## Setup

1. Clone the repo:
   ```bash
   git clone https://github.com/<your-username>/python-projects.git
   ```

2. For projects that require environment variables (Day 39–40, Day 69), create a `.env` file in the project folder with the required keys. See each project's source for the expected variable names.

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```