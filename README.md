# LangGraph-Chatbot

AI-powered chatbot built with Django REST Framework, LangChain, and LangGraph. Implements a DAG-based conversational flow with memory, decision logic, and OpenAI GPT integration. Fully containerized using Docker for seamless deployment and scalability.

---

## 🚀 Quickstart

### 1. Clone the Repository

```sh
git clone https://github.com/aniketsuryawanshi1/LangGraph-Chatbot.git
cd LangGraph-Chatbot
```

---

### 2. Configure Environment Variables

Copy the example `.env` file and edit it with your own settings:

```sh
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set your OpenAI API key and database credentials as needed.

---

### 3. Create a Python Virtual Environment (for local development)

```sh
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### 4. Build Docker Containers

From the project root:

```sh
docker compose build
```

---

### 5. Run Database Migrations

```sh
docker compose run backend python manage.py makemigrations
docker compose run backend python manage.py migrate
```

---

### 6. Start the Application

```sh
docker compose up
```

The backend will be available at [http://localhost:8000](http://localhost:8000).

---

## 🧪 API Testing

- **Health Check:**  
  `GET http://localhost:8000/api/chat/health/`

- **Chat Endpoint:**  
  `POST http://localhost:8000/api/chat/`  
  Body (JSON):
  ```json
  {
    "query": "Hello, how are you?"
  }
  ```

---

## 📝 Notes

- Make sure your OpenAI API key has quota.
- For any issues, check the logs in `backend/logs/django.log`.

---
