# GitHub Webhook Handler

This project is a Flask-based application that handles GitHub webhook events (`push`, `pull_request`, and `merge`). It stores these events in a MongoDB database and provides APIs to fetch the latest events. It has UI that poll all events from database and display 10 most recent events.

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
```

---

### **2. Install Dependencies**
```bash
pip install -r requirements.txt
```

---

### **3. Configure MongoDB**
1. **Ensure MongoDB is installed**:
   - Download MongoDB from the [official MongoDB website](https://www.mongodb.com/try/download/community) or use a package manager like Chocolatey.
   - Install MongoDB and start the service:
     ```bash
     net start MongoDB
     ```
2. **Default Configuration**:
   - MongoDB runs on `mongodb://localhost:27017`.
   - The database name is `github_webhooks`, and the collection name is `events`.

---

### **4. Configure ngrok for Webhook URL**

1. **Install ngrok**:
   - Download ngrok for Windows from the [ngrok website](https://ngrok.com/download).
   - Alternatively, use Chocolatey:
     ```bash
     choco install ngrok
     ```

2. **Authenticate ngrok** (if you have an account):
   ```bash
   ngrok config add-authtoken <your_auth_token>
   ```
   - Replace `<your_auth_token>` with the token from your ngrok account.

3. **Start ngrok**:
   ```bash
   ngrok http 5000
   ```
   - This will generate a public forwarding URL like `https://<random-string>.ngrok.io`.

4. **Keep ngrok Running**:
   - Leave the terminal running to maintain the tunnel.

---

### **5. Add Webhook URL to GitHub**

1. Open your GitHub repository.
2. Navigate to:
   **Settings** > **Webhooks** > **Add webhook**.
3. Configure the webhook:
   - **Payload URL**: Use the ngrok URL followed by your Flask route:
     ```
     https://<random-string>.ngrok.io/api/v1/github-webhook
     ```
   - **Content type**: Set to `application/json`.
   - **Secret**: Optionally, add a secret for securing the webhook.
   - **Events**: Select the events you want to listen to (e.g., `push`, `pull_request`, `merge`).
4. Save the webhook.

---

### **6. Run the Application**

1. Start your Flask app:
   ```bash
   set PYTHONPATH=%cd%
   python app.py
   ```
2. The app will be accessible locally at:
   ```
   http://127.0.0.1:5000
   ```
3. ngrok will forward traffic from the public URL to this local address.

---

### **7. Test the Webhook**
- Trigger an event (e.g., push a commit, open a pull request).
- Check the Flask app logs to confirm the webhook event was received:
  ```bash
  Received GitHub event: { ... }
  ```

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
      "merged_at": "2025-01-16T09:00:00Z"
    }
  }
  ```

- **Response**:
  - `200 OK`: Event processed successfully.
  - `400 Bad Request`: Unsupported event type.
  - `500 Internal Server Error`: Error while processing the webhook.

---

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