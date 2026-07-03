# CallsRM

CallsRM is an open-source WhatsApp Business API CRM backend that captures messages and calls as first-class citizens.

## The Problem

When building WhatsApp automations with n8n, you need a CRM as an intermediary between Meta and n8n to visualize and manage conversations. Most options are fully paid. Chatwoot is the most popular open-source alternative — but it has a critical gap.

Since July 2025, Meta's WhatsApp Business API supports native voice calls. Chatwoot receives these call webhooks in their Community Edition but silently ignores them — confirmed in their own codebase and GitHub issues. Their team stated that voice is an Enterprise-only feature (issue #11511, PR #13841 closed).

CallsRM fills that gap: an open-source CRM that handles both messages and calls natively, designed to work alongside n8n automations.

## Stack

- **FastAPI** — async Python backend
- **PostgreSQL** — relational database
- **SQLModel** — ORM (SQLAlchemy + Pydantic)
- **Docker** — containerization

## Getting Started

```bash
cp .env.example .env
# fill in your credentials in .env
docker-compose up
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/webhooks` | Receive Meta webhook events |
| GET | `/contacts` | List all contacts |
| GET | `/contacts/{id}/messages` | Message history for a contact |
| GET | `/contacts/{id}/calls` | Call history for a contact |

## Roadmap

- [x] Receive and store incoming messages
- [x] Receive and store incoming calls
- [x] Auto-create contacts on first interaction
- [x] REST API to query contacts, messages and calls
- [x] Forward events to n8n in real time
- [x] Send WhatsApp messages via Meta API
- [x] POST /n8n/callback for automated responses
- [ ] Layered architecture refactor (routes → controller → service)
- [ ] Response schemas (DTOs)
- [ ] Unit tests with pytest
- [ ] Postman collection
- [ ] Auth/JWT
- [ ] Live call handling via WebRTC (Meta Calling API)

## License

MIT