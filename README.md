# Kost Microservices AFL-3

## Project Description

This project is a simple implementation of a microservices architecture for a Boarding House Management System. The system was developed to fulfill the AFL-3 assignment for the Microservices Development course.

The system consists of several small services that run independently using Docker Compose. Each service has its own responsibility, such as authentication, room management, tenant data management, payment management, maintenance handling, notification, and monitoring.

## Main Features

* Traefik as the API Gateway
* REST API as the main communication method
* Auth Middleware for simple token validation
* RabbitMQ as the message broker
* Notification Service for receiving events
* WebSocket Service as a simulation of live push notification
* Container monitoring using cAdvisor
* Host monitoring using Node Exporter
* Prometheus for metrics scraping
* Grafana for dashboard visualization

## Service Architecture

Main services:

* Auth Service
* Room Service
* Tenant Service
* Payment Service
* Maintenance Service
* Auth Middleware
* RabbitMQ
* Notification Service
* WebSocket Service
* Prometheus
* Grafana
* cAdvisor
* Node Exporter
* Traefik API Gateway

## How to Run the Project

Make sure Docker Desktop is already running.

Run the following command from the root folder of the project:

```bash
docker compose up --build
```

To stop all containers, run:

```bash
docker compose down
```

## REST API Endpoints

### Auth Service

Health check:

```http
GET http://localhost/auth/health
```

Login:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost/auth/login" -ContentType "application/json" -Body '{"username":"admin","password":"admin123"}'
```

The login response will return this token:

```text
demo-jwt-token
```

### Auth Middleware

Test without token:

```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost/private/health"
```

Test with token:

```powershell
Invoke-RestMethod -Method GET -Uri "http://localhost/private/health" -Headers @{ Authorization = "Bearer demo-jwt-token" }
```

### Room Service

```http
GET http://localhost/rooms
```

### Tenant Service

```http
GET http://localhost/tenants
```

### Payment Service

```http
GET http://localhost/payments
POST http://localhost/payments/pay
```

PowerShell test:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost/payments/pay"
```

### Maintenance Service

```http
GET http://localhost/maintenance
POST http://localhost/maintenance/update
```

PowerShell test:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost/maintenance/update"
```

## Event and Notification Flow

The Payment Service and Maintenance Service publish events to RabbitMQ. The Notification Service consumes those events and forwards them to the WebSocket Service.

Check notifications:

```http
GET http://localhost/notifications
```

Check WebSocket/live push simulation:

```http
GET http://localhost/websocket/messages
```

## Monitoring

### RabbitMQ Management

```text
http://localhost:15672
```

Login:

```text
Username: admin
Password: admin123
```

### Prometheus

```text
http://localhost:9090
```

Prometheus targets:

```text
http://localhost:9090/targets
```

### Grafana

```text
http://localhost:3000
```

Default login:

```text
Username: admin
Password: admin
```

Grafana may ask the user to change the password after the first login.

### cAdvisor

```text
http://localhost:8081
```

### Node Exporter Metrics

```text
http://localhost:9100/metrics
```

## Rubric Compliance Evidence

| Criteria                                 | Status    |
| ---------------------------------------- | --------- |
| Microservice architecture design         | Completed |
| More than 10 containers                  | Completed |
| REST API                                 | Completed |
| WebSocket / Message Broker               | Completed |
| Host monitoring                          | Completed |
| Container monitoring                     | Completed |
| Traefik API Gateway                      | Completed |
| Authentication middleware                | Completed |
| Services communicate with each other     | Completed |
| Automatic deployment with Docker Compose | Completed |

## Project Structure

```text
kost-microservices-afl3/
├── docker-compose.yml
├── monitoring/
│   └── prometheus.yml
├── middleware/
│   └── auth-middleware/
├── services/
│   ├── auth-service/
│   ├── room-service/
│   ├── tenant-service/
│   ├── payment-service/
│   ├── maintenance-service/
│   ├── notification-service/
│   └── websocket-service/
```

## Technologies Used

* Docker
* Docker Compose
* Traefik
* RabbitMQ
* Prometheus
* Grafana
* cAdvisor
* Node Exporter
* REST API
* WebSocket



## Conclusion

This project demonstrates how a boarding house management system can be designed using a microservices architecture. By separating the system into multiple independent services, each service can focus on a specific responsibility. Docker Compose makes the system easier to run, while Traefik, RabbitMQ, WebSocket, and monitoring tools help demonstrate important concepts in microservices development.
