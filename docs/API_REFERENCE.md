# API Reference

## Base URL
`/api`

## Endpoints

### `GET /health`
Returns the health status of the API.
**Response:**
```json
{
  "status": "healthy"
}
```

### `GET /api/suggestions`
Provides autocomplete suggestions for books based on the given query.
**Parameters:**
- `q` (string): The search query (minimum 3 characters).

**Response:**
```json
{
  "suggestions": [
    "Python Crash Course",
    "Effective Python"
  ]
}
```

### `POST /api/chat`
Main endpoint for natural language queries from the OPAC UI.
**Request Body:**
```json
{
  "message": "Find Python books"
}
```

**Response:**
Returns an HTML string containing the rendered book cards or a specific message.
```json
{
  "response": "<h3>Search Results (5)</h3>..."
}
```
