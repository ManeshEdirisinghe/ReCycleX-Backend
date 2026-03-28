# ReCycleX Backend — README

> **FastAPI** · **MySQL** · **SQLAlchemy** · **Alembic** · **JWT Auth** · **Role-Based Access**

---

## Overview

ReCycleX is an e-waste management platform backend built with FastAPI. It handles the full lifecycle of e-waste items — from user submission, admin review, agent pickup, center processing, through to reward issuance and certificate generation.

---

## Setup

### Prerequisites
- Python 3.11+
- MySQL 8+

### 1. Clone and create virtual environment
```bash
git clone <repo-url>
cd ReCycleX-backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root:

```env
# Database
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=recyclex

# JWT
SECRET_KEY=your-secure-random-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080

# Seeding
FIRST_SUPERUSER_EMAIL=admin@recyclex.com
FIRST_SUPERUSER_PASSWORD=your-admin-password

# CORS
BACKEND_CORS_ORIGINS=["http://localhost:3000","http://localhost:5173"]
```

> **IMPORTANT:** Replace `SECRET_KEY` and superuser password before deploying. Never commit `.env`.

### 4. Create the MySQL database
```sql
CREATE DATABASE recyclex CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

---

## Database Migrations

Migrations use **Alembic** with manual chained versioning.

### Apply all migrations
```bash
alembic upgrade head
```

### Migration chain
| # | File | Description |
|---|------|-------------|
| 1 | `1_initial_users.py` | `users` table |
| 2 | `2_add_items_categories.py` | `categories`, `items` tables |
| 3 | `3_add_pickup_requests.py` | `pickup_requests` table |
| 4 | `4_add_processing_centers.py` | `processing_centers` + `assigned_center_id` on items |
| 5 | `5_add_processing.py` | `item_processing` table |
| 6 | `6_add_rewards_certificates.py` | `rewards`, `certificates` tables |

### Rollback one step
```bash
alembic downgrade -1
```

---

## Running the Server

```bash
# Seed the admin account (first time only)
python -m app.initial_data

# Start development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

| URL | Description |
|-----|-------------|
| `http://localhost:8000/` | Health check |
| `http://localhost:8000/docs` | Swagger UI |
| `http://localhost:8000/redoc` | ReDoc |

---

## Environment Variables

| Variable | Default | Notes |
|----------|---------|-------|
| `MYSQL_USER` | `root` | |
| `MYSQL_PASSWORD` | _(empty)_ | |
| `MYSQL_HOST` | `localhost` | |
| `MYSQL_PORT` | `3306` | |
| `MYSQL_DB` | `recyclex` | |
| `SECRET_KEY` | _(hardcoded)_ | **Override in production** |
| `ALGORITHM` | `HS256` | |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `10080` (7 days) | |
| `FIRST_SUPERUSER_EMAIL` | `admin@recyclex.com` | Used by seed script |
| `FIRST_SUPERUSER_PASSWORD` | `admin` | **Override in production** |
| `BACKEND_CORS_ORIGINS` | localhost:3000, 5173 | JSON array of allowed origins |

---

## User Roles

| Role | Capabilities |
|------|-------------|
| `USER` | Submit items, request pickups, view rewards/certificates |
| `ADMIN` | Full platform control |
| `PICKUP_AGENT` | View assigned pickups, update pickup status |
| `RECYCLING_CENTER` | View/process assigned items for recycling |
| `REPAIR_CENTER` | View/process assigned items for repair |

---

## API Endpoint Catalog

All routes prefixed with `/api/v1`.

### Auth
| Method | Path | Access |
|--------|------|--------|
| POST | `/auth/register` | Public |
| POST | `/auth/login` | Public |
| GET | `/auth/me` | Authenticated |

### Users
| Method | Path | Access |
|--------|------|--------|
| GET | `/users/profile` | Authenticated |

### Categories
| Method | Path | Access |
|--------|------|--------|
| GET | `/categories/` | Public |

### Items
| Method | Path | Access |
|--------|------|--------|
| POST | `/items/` | User |
| GET | `/items/my-items` | Owner |
| GET | `/items/{item_id}` | Owner / Admin |
| PUT | `/items/{item_id}` | Owner / Admin |
| DELETE | `/items/{item_id}` | Owner / Admin |

### Pickups
| Method | Path | Access |
|--------|------|--------|
| POST | `/pickups/` | User (item owner) |
| GET | `/pickups/my-pickups` | Owner |
| GET | `/pickups/{pickup_id}` | Owner / Admin / Assigned Agent |

### Agent
| Method | Path | Access |
|--------|------|--------|
| GET | `/agent/pickups` | Pickup Agent |
| PUT | `/agent/pickups/{pickup_id}/status` | Assigned Agent |

### Center
| Method | Path | Access |
|--------|------|--------|
| GET | `/center/profile` | Center User |
| GET | `/center/items` | Center User |

### Processing
| Method | Path | Access |
|--------|------|--------|
| POST | `/processing/` | Center User |
| PUT | `/processing/{processing_id}` | Center User |
| GET | `/processing/item/{item_id}` | Owner / Admin / Center |

### Rewards
| Method | Path | Access |
|--------|------|--------|
| GET | `/rewards/my-rewards` | Authenticated |
| GET | `/rewards/my-points` | Authenticated |

### Certificates
| Method | Path | Access |
|--------|------|--------|
| GET | `/certificates/my-certificates` | Authenticated |

### Admin
| Method | Path | Access |
|--------|------|--------|
| GET | `/admin/items` | Admin |
| PUT | `/admin/items/{item_id}/approve` | Admin |
| PUT | `/admin/items/{item_id}/reject` | Admin |
| PUT | `/admin/items/{item_id}/assign-center` | Admin |
| POST | `/admin/categories` | Admin |
| PUT | `/admin/pickups/{pickup_id}/approve` | Admin |
| PUT | `/admin/pickups/{pickup_id}/assign-agent` | Admin |
| POST | `/admin/centers` | Admin |
| GET | `/admin/centers` | Admin |
| GET | `/admin/dashboard` | Admin |

---

## Error Response Format

All errors return a consistent JSON envelope:

```json
{
  "success": false,
  "error": {
    "code": "NOT_FOUND",
    "message": "Item not found",
    "details": null
  }
}
```

Validation errors include field-level breakdown:

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Input validation failed",
    "details": {
      "errors": [
        { "field": "body.email", "message": "value is not a valid email address", "type": "value_error" }
      ]
    }
  }
}
```

---

## State Transitions

### Item Status
```
PENDING_REVIEW → APPROVED / REJECTED
APPROVED → PICKUP_REQUESTED (user requests pickup)
PICKUP_REQUESTED → READY_FOR_PICKUP (admin approves)
READY_FOR_PICKUP → PICKED_UP (agent confirms pickup)
PICKED_UP → ASSIGNED_TO_CENTER (admin assigns center)
ASSIGNED_TO_CENTER → IN_PROCESSING (center starts work)
IN_PROCESSING → COMPLETED (center submits final status)
```

### Pickup Status
```
REQUESTED → APPROVED → ASSIGNED → IN_TRANSIT → PICKED_UP → COMPLETED
                                                          ↘ CANCELED
```

---

## Reward & Certificate Trigger Logic

When a center completes processing with `final_status` of `RECYCLED`, `REPAIRED`, or `DONATED`:
1. The item's linked **category** `base_reward_points` are awarded to the item owner as a **Reward**.
2. A **Certificate** is auto-generated with a unique reference number (`CERT-YYYYMMDD-XXXXXX`).
3. Item status moves to `COMPLETED`.

---

## Project Structure

```
ReCycleX-backend/
├── app/
│   ├── main.py                    # FastAPI app, CORS, exception handlers
│   ├── initial_data.py            # Admin seeding script
│   ├── api/
│   │   ├── api.py                 # APIRouter aggregator
│   │   ├── deps.py                # Shared FastAPI dependencies (auth, db)
│   │   └── endpoints/             # Feature-grouped route handlers (11 modules)
│   ├── core/
│   │   ├── config.py              # pydantic-settings config
│   │   ├── exceptions.py          # Custom exception classes
│   │   ├── security.py            # JWT + bcrypt utilities
│   │   └── init_db.py             # DB init hook
│   ├── db/
│   │   ├── base_class.py          # DeclarativeBase + auto timestamps
│   │   └── session.py             # SQLAlchemy session factory
│   ├── models/                    # 9 SQLAlchemy ORM models
│   ├── schemas/                   # 10 Pydantic DTO modules
│   ├── services/                  # 9 service/business logic modules
│   └── utils/                     # Utilities (placeholder for future helpers)
├── alembic/
│   └── versions/                  # 6 chained migration scripts
├── .env                           # Environment config (not committed)
├── alembic.ini
├── requirements.txt
└── README.md
```

---

## Recommended Next Improvements

- [ ] Unit and integration tests (`pytest` + `httpx`)
- [ ] Rate limiting on auth endpoints (`slowapi`)
- [ ] Refresh token support
- [ ] Email notifications for key status changes
- [ ] PDF certificate generation (`reportlab` or `weasyprint`)
- [ ] Pagination metadata wrapper `{ items, total, page, size }`
- [ ] Soft delete for items / users
- [ ] Admin user management endpoints (create/deactivate by role)
- [ ] S3/cloud storage for item `image_url`
- [ ] Structured request logging with correlation IDs
- [ ] Docker + docker-compose setup
- [ ] CI/CD pipeline (GitHub Actions)

---

## Author

Developed for the **ReCycleX** e-waste management project.
