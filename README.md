# GitHub Webhook Handler

This project is a Flask-based application that handles GitHub webhook events (`push`, `pull_request`, and `merge`). It stores these events in a MongoDB database and provides APIs to fetch the latest events.

---

## **Project Structure**

```
github-webhook/
├── app.py                      # Main entry point of the application
├── controller/
│   └── webhook_controller.py   # Controller to register routes and handle API requests
├── service/
│   └── github_webhook_service.py  # Service layer for business logic and MongoDB interactions
├── model/
│   └── github_webhook_model.py  # MongoDB model and database operations
├── static/
│   ├── app.js                 # Frontend JavaScript for UI interactions
│   └── style.css              # Frontend styles
├── templates/
│   └── html.html              # Frontend HTML template
├── utils/
│   └── logger.py              # Logger utility for consistent logging
├── requirements.txt           # Project dependencies
├── README.md                  # Project documentation
```

---

## **Features**

1. **Webhook Handling**
   - Supports GitHub webhook events: `push`, `pull_request`, and `merge`.
   - Parses payloads and saves event data in MongoDB.

2. **APIs**
   - `POST /api/v1/github-webhook`: Handles incoming webhook events.
   - `GET /api/v1/latest-events`: Fetches the latest events from the database.

3. **Frontend**
   - Minimal frontend for displaying events, styled with `style.css` and powered by `app.js`.

4. **Logging**
   - All operations are logged for easier debugging and maintenance.

---

## **Setup Instructions**

### **1. Clone the Repository**
```bash
git clone <repository_url>
cd github-webhook
```

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Configure MongoDB**
- Ensure MongoDB is running locally.
- Default connection: `mongodb://localhost:27017`.
- The database name is `github_webhooks`, and the collection name is `events`.

### **5. Run the Application**
```bash
python app.py
```

- The application will run on `http://127.0.0.1:5000`.

---

## **API Endpoints**

### **1. Handle Webhook Events**
- **Endpoint**: `POST /api/v1/github-webhook`
- **Headers**:
  - `Content-Type`: `application/json`
  - `x-github-event`: Event type (`push`, `pull_request`, `merge`)
- **Request Body**: GitHub webhook payload (varies by event type).

#### **Example Payloads**

- **Push Event**:
  ```json
  {
    "ref": "refs/heads/main",
    "head_commit": {
      "author": {
        "name": "user3"
      },
      "timestamp": "2025-01-15T22:15:46+05:30"
    }
  }
  ```

- **Pull Request Event**:
  ```json
  {
    "action": "opened",
    "pull_request": {
      "user": {
        "login": "user2"
      },
      "head": {
        "ref": "feature-branch"
      },
      "base": {
        "ref": "main"
      },
      "created_at": "2025-01-16T09:02:00Z"
    }
  }
  ```

- **Merge Event**:
  ```json
  {
    "action": "closed",
    "pull_request": {
      "merged": true,
      "user": {
        "login": "user1"
      },
      "head": {
        "ref": "feature-branch"
      },
      "base": {
        "ref": "main"
      },
      "merged_at": "2026-01-16T09:00:00Z"
    }
  }
  ```

- **Response**:
  - `200 OK`: Event processed successfully.
  - `400 Bad Request`: Unsupported event type.
  - `500 Internal Server Error`: Error while processing the webhook.

### **2. Fetch Latest Events**
- **Endpoint**: `GET /api/v1/latest-events`
- **Response**:
  - `200 OK`: List of latest events.
  - `500 Internal Server Error`: Error while fetching events.

---

## **Technologies Used**
- **Backend**: Flask
- **Database**: MongoDB
- **Frontend**: HTML, CSS, JavaScript
- **Logging**: Python's `logging` module

---

## **Acknowledgments**
This project is designed for handling GitHub webhooks and demonstrates a structured approach to Flask application development.

