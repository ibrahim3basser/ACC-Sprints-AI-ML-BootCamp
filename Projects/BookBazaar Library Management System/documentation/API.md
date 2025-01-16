# BookBazaar API Documentation

## Overview

BookBazaar is a library management system that provides RESTful APIs for managing books, authors, stock, and sales.

## Base URL

http://127.0.0.1:5000

## Endpoints

### Books

#### Get All Books

GET /books

**Response**
[
{
"id": 1,
"title": "1984",
"author_id": 1,
"genre": "Dystopian",
"published_year": 1949,
"price": 9.99
},
{
"id": 2,
"title": "Harry Potter",
"author_id": 2,
"genre": "Fantasy",
"published_year": 1997,
"price": 14.99
}
]

#### Get Book by ID

GET /books/<id>

**Response**
{
"id": 1,
"title": "1984",
"author_id": 1,
"genre": "Dystopian",
"published_year": 1949,
"price": 9.99
}

#### Create New Book

POST /books

**Request Body**
{
"title": "New Book",
"author_id": 1,
"genre": "Fiction",
"published_year": 2023,
"price": 19.99
}

**Response**
{
"id": 3,
"message": "Book created successfully"
}

### Authors

#### Get All Authors

GET /authors

**Response**
[
{
"id": 1,
"name": "George Orwell",
"country": "United Kingdom",
"birthdate": "1903-06-25"
},
{
"id": 2,
"name": "J.K. Rowling",
"country": "United Kingdom",
"birthdate": "1965-07-31"
}
]

#### Get Author by ID

GET /authors/<id>

**Response**
{
"id": 1,
"name": "George Orwell",
"country": "United Kingdom",
"birthdate": "1903-06-25"
}

#### Create New Author

POST /authors

**Request Body**
{
"name": "New Author",
"country": "USA",
"birthdate": "1990-01-01"
}

**Response**
{
"id": 3,
"message": "Author created successfully"
}

### Stock

#### Get Stock by Book ID

GET /stock/<book_id>

**Response**
{
"id": 1,
"book_id": 1,
"quantity": 10
}

#### Update Stock

PUT /stock/<book_id>

**Request Body**
{
"quantity": 15
}

**Response**
{
"message": "Stock updated successfully"
}

### Sales

#### Create New Sale

POST /sales

**Request Body**
{
"book_id": 1,
"user_id": 1,
"quantity": 2
}

**Response**
{
"id": 1,
"message": "Sale created successfully"
}

#### Get User Sales

GET /sales/user/<user_id>

**Response**
[
{
"id": 1,
"book_id": 1,
"user_id": 1,
"quantity": 2,
"sale_date": "2023-11-15T10:30:00",
"total_price": 19.98
}
]

## Error Responses

### 400 Bad Request

{
"error": "Missing required fields"
}

### 404 Not Found

{
"error": "Book not found"
}

### 500 Internal Server Error

{
"error": "An unexpected error occurred"
}

## Status Codes

The API uses the following status codes:

- 200 - Success
- 201 - Created
- 400 - Bad Request
- 404 - Not Found
- 500 - Internal Server Error

## Sample Usage

### JavaScript Fetch Example

// Get all books
fetch('http://127.0.0.1:5000/books')
.then(response => response.json())
.then(data => console.log(data));

// Create new book
fetch('http://127.0.0.1:5000/books', {
method: 'POST',
headers: {
'Content-Type': 'application/json'
},
body: JSON.stringify({
title: "New Book",
author_id: 1,
genre: "Fiction",
published_year: 2023,
price: 19.99
})
})
.then(response => response.json())
.then(data => console.log(data));

### Python Requests Example

import requests

# Get all books

response = requests.get('http://127.0.0.1:5000/books')
books = response.json()

# Create new book

new_book = {
"title": "New Book",
"author_id": 1,
"genre": "Fiction",
"published_year": 2023,
"price": 19.99
}
response = requests.post('http://127.0.0.1:5000/books', json=new_book)
result = response.json()

## Rate Limiting

- 100 requests per minute per IP address

## Notes

- All timestamps are in UTC
- Prices are in USD
- Date format: YYYY-MM-DD
