# BookBazaar Setup Guide

## Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- SQLite3

## Project Structure

BookBazaar/
│
├── config/
│ ├── **init**.py
│ └── config.py
│
├── database/
│ ├── **init**.py
│ ├── bookbazaar.db
│ └── schema.sql
│
├── app/
│ ├── **init**.py
│ ├── models/
│ │ ├── **init**.py
│ │ ├── book.py
│ │ ├── author.py
│ │ ├── user.py
│ │ ├── stock.py
│ │ └── sale.py
│ │
│ └── services/
│ ├── **init**.py
│ ├── sqlite_service.py
│ ├── book_service.py
│ ├── author_service.py
│ ├── stock_service.py
│ └── sale_service.py
│
├── api/
│ ├── **init**.py
│ └── routes/
│ ├── **init**.py
│ ├── book_routes.py
│ ├── author_routes.py
│ ├── stock_routes.py
│ └── sale_routes.py
│
├── docs/
│ ├── api.md
│ └── setup.md
│
├── requirements.txt
├── run.py
└── README.md

## Installation Steps

# Windows

python -m venv venv
venv\Scripts\activate

# Linux/MacOS

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python init_db.py

## runing appp

python run.py

```

```
