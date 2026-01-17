 ....Distributed Task Queue (Python + REST)

A lightweight, distributed background task processing system inspired by production-grade work queues.

 ....Features

REST-based task submission & monitoring

Redis-backed distributed queue

Concurrent worker pool

Task cancellation support

Pluggable task handlers

Basic monitoring & metrics

Horizontally scalable workers

 ....Architecture

API Service: Accepts client requests and enqueues tasks

Redis: Stores tasks, metadata, and queue state

Worker Service: Fetches and executes tasks asynchronously

Client CLI: Submits and manages tasks via HTTP

 Task Lifecycle

Client submits task via REST API

Task stored in Redis queue

Worker picks up task

Status updated throughout execution

Result stored and retrievable

🌐 REST API Overview
Method	Endpoint	Description
POST	/tasks	Submit a new task
GET	/tasks/{id}	Fetch task status
DELETE	/tasks/{id}	Cancel a task
GET	/metrics	Queue & worker stats

🛠 Tech Stack

Python

Redis

FastAPI / Flask

Docker (optional)

HTTP REST

📈 Scalability

Multiple API instances supported

Workers scale horizontally

Redis acts as a shared coordination layer

.... Future Improvements

Retry policies & dead-letter queue

Authentication & rate limiting

Priority queues

Web dashboard

Persistence layer for long-term storage