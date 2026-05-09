AI Lead Processing System
Overview

This project is a backend system that simulates how modern AI-powered CRM platforms process leads reliably at scale.

The system accepts incoming leads through a FastAPI API, stores them in MySQL, pushes processing tasks into a Redis queue, and asynchronously processes those tasks using OpenAI.

The focus of the project is not just AI integration, but building reliable infrastructure around AI workflows. The project demonstrates concepts like queue-based processing, retries, rate limiting, worker systems, observability, and webhook communication.

Problem Being Solved

Calling AI APIs directly from a web request is usually a bad idea in production systems because:

  
  •	AI APIs are slow

  •	requests can fail randomly

  •	providers enforce rate limits

  •	traffic spikes can overload the system

  •	failed requests can cause task loss

This project solves that problem by separating the API layer from the AI processing layer using Redis queues and background workers.

How the System Works
1.	A client sends a lead to the FastAPI API.
2.	The API stores the lead in MySQL.
3.	A processing task is created and pushed into Redis.
4.	A worker continuously listens to the queue.
5.	The worker processes the lead using OpenAI.
6.	The lead is classified as hot, warm, or cold.
7.	Task status is updated in the database.
8.	A webhook notification is sent after processing completes.

Architecture

Client

   ↓
  
FastAPI API

   ↓
  
MySQL Database

   ↓
  
Redis Queue

   ↓
  
Worker

   ↓
  
OpenAI API

   ↓
  
Webhook Notification

Features
1. Lead Management API

   The API accepts lead information and stores it in MySQL.

2. Redis Queue

   Redis is used as a task queue to decouple API requests from AI processing.

   This improves:
  
    •	Scalability
  
    •	reliability
  
    •	response time
  
    •	fault tolerance

   Instead of processing AI requests immediately, tasks are queued and processed  asynchronously.

3. Worker-Based Processing

   A dedicated worker consumes tasks from Redis and processes them independently.

    This allows:
  
     •	background processing
  
     •	retry handling
  
     •	controlled AI execution
  
     •	better system scalability

4. Worker-Based Processing

    A dedicated worker consumes tasks from Redis and processes them independently.
     This allows:
  
     •	background processing
  
     •	retry handling
  
     •	controlled AI execution
  
   •	better system scalability

5. Retry Mechanism

     Temporary AI failures are retried automatically.

     The system uses exponential backoff:
  
     •	first retry → 1 second
  
     •	second retry → 2 seconds
  
     •	third retry → 4 seconds

    This improves reliability during unstable API conditions.

6. Rate Limiting

      The worker uses a custom rate limiter to prevent excessive API calls.

      This simulates real-world production environments where providers enforce request limits.

7. Metrics Endpoint

      The project exposes operational metrics through:

     GET /metrics
     This helps monitor:
   
      •	queue health
   
      •	worker activity
   
      •	failures
   
      •	processing state

8. Webhook Integration

    After lead processing completes, the system sends webhook notifications to external services.
    Webhook.site was used during development to test webhook delivery.

Tech Stack
Backend Framework:

•	FastAPI

Database:

•	MySQL

ORM:

•	SQLAlchemy

Queue:

•	Redis

AI Provider:

•	OpenAI API

Worker System:

•	Python background worker

Environment Management:

•	python-dotenv

Webhook Requests:

•	requests

Project Structure
app/

│

├── database/

│   ├── db.py

│   ├── model.py

│

├── api/routes/

│   ├── leads.py

│   ├── metrics.py

│   ├── dashboard.py

│

├── schema/

│   ├── lead.py

│

├── queue/

│   ├── client.py

│   ├── producer.py

│

├── workers/

│   ├── worker.py

│   ├── retry.py

│   ├── ratelimiter.py

│

├── services/

│   ├── aiservice.py

│   ├── webhook.py

│

├── main.py

├── .env

├── readme.md

├── requirements.txt

├── .gitignore


Running the Project
Start Redis
        
    docker run -d -p 6379:6379 redis
Start FastAPI
  
    uvicorn app.main:app --reload
Start Worker
      
      python -m app.workers.worker




API Endpoints

Create Lead:
POST /leads

Get Leads:
GET /leads

Metrics:
GET /metrics




Concepts Demonstrated

  This project demonstrates:

  •	asynchronous task processing
  
  •	distributed worker systems
  
  •	AI orchestration
  
  •	retry handling

  •	rate limiting
  
  •	queue-based architecture
  
  •	webhook communication
  
  •	observability and monitoring
  
  •	production-style backend design


Final Note

  The main goal of this project was to build reliable infrastructure around AI workflows rather than building a simple CRUD    application with AI added on top.
  
  The project focuses heavily on scalability, fault tolerance, asynchronous processing, and production-style backend           architecture.


