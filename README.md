# ReCycleX Backend (FastAPI)

## Overview
ReCycleX is a backend service for managing e-waste collection, pickup, repair, donation, and recycling workflows. This FastAPI version provides a clean REST API for authentication, item management, pickup handling, processing center operations, rewards, and certificates.

## Tech Stack
- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy
- Alembic
- MySQL or PostgreSQL
- Pydantic
- JWT Authentication
- Passlib / bcrypt

## Core Features
- User registration and login
- JWT-based authentication
- Role-based access control
- E-waste item management
- Pickup request workflow
- Admin assignment for pickup agents and centers
- Repair / recycling processing updates
- Rewards and certificate support
- Swagger API documentation

## User Roles
- **ADMIN** – manages users, items, pickups, and center assignments
- **USER** – registers items, requests pickups, tracks item status
- **PICKUP_AGENT** – handles assigned pickup requests
- **RECYCLING_CENTER** – updates recycling progress for assigned items
- **REPAIR_CENTER** – updates repair progress for assigned items

## Suggested Project Structure
```bash
recyclex-backend/
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py
│   │   ├── security.py
│   │   └── database.py
│   ├── api/
│   │   ├── deps.py
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── items.py
│   │       ├── pickups.py
│   │       ├── processing.py
│   │       ├── rewards.py
│   │       └── admin.py
│   ├── models/
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── category.py
│   │   ├── pickup.py
│   │   ├── center.py
│   │   ├── processing.py
│   │   ├── reward.py
│   │   └── certificate.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── item.py
│   │   ├── pickup.py
│   │   ├── processing.py
│   │   ├── reward.py
│   │   └── common.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── item_service.py
│   │   ├── pickup_service.py
│   │   ├── processing_service.py
│   │   └── reward_service.py
│   └── utils/
│       ├── enums.py
│       └── helpers.py
├── alembic/
├── tests/
├── .env
├── requirements.txt
├── alembic.ini
└── README.md
```

## Installation
### 1. Clone the repository
```bash
git clone <your-repo-url>
cd recyclex-backend
```

### 2. Create a virtual environment
```bash
python -m venv venv
```

### 3. Activate the virtual environment
**Windows**
```bash
venv\Scripts\activate
```

**macOS / Linux**
```bash
source venv/bin/activate
```

### 4. Install dependencies
```bash
pip install -r requirements.txt
```

## Example `requirements.txt`
```txt
fastapi
uvicorn[standard]
sqlalchemy
alembic
pydantic
pydantic-settings
python-jose[cryptography]
passlib[bcrypt]
pymysql
psycopg2-binary
python-multipart
email-validator
```

## Environment Variables
Create a `.env` file in the project root.

```env
APP_NAME=ReCycleX Backend
APP_ENV=development
APP_DEBUG=true
API_V1_PREFIX=/api/v1
SECRET_KEY=your_super_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/recyclex_db
```

For PostgreSQL:
```env
DATABASE_URL=postgresql+psycopg2://postgres:password@localhost:5432/recyclex_db
```

## Running the Server
```bash
uvicorn app.main:app --reload
```

Server will run at:
```bash
http://127.0.0.1:8000
```

Swagger documentation:
```bash
http://127.0.0.1:8000/docs
```

ReDoc documentation:
```bash
http://127.0.0.1:8000/redoc
```

## Database Migrations
Initialize Alembic:
```bash
alembic init alembic
```

Create migration:
```bash
alembic revision --autogenerate -m "initial schema"
```

Apply migrations:
```bash
alembic upgrade head
```

## Main Modules
### Authentication
- Register user
- Login user
- Generate JWT token
- Get current logged-in user

### E-Waste Items
- Add item
- Update item
- Delete item
- Get own items
- Admin get all items

### Pickup Requests
- Create pickup request
- View own pickup requests
- Admin approve pickup
- Admin assign pickup agent
- Agent update pickup status

### Processing
- Assign item to repair or recycling center
- Update processing status
- Track final outcome

### Rewards & Certificates
- Award eco points after successful completion
- View reward history
- Support future certificate generation

## Example API Endpoints
### Auth
- `POST /api/v1/auth/register`
- `POST /api/v1/auth/login`
- `GET /api/v1/auth/me`

### Items
- `POST /api/v1/items`
- `GET /api/v1/items/my-items`
- `GET /api/v1/items/{item_id}`
- `PUT /api/v1/items/{item_id}`
- `DELETE /api/v1/items/{item_id}`

### Pickups
- `POST /api/v1/pickups`
- `GET /api/v1/pickups/my-pickups`
- `GET /api/v1/pickups/{pickup_id}`

### Admin
- `GET /api/v1/admin/items`
- `PUT /api/v1/admin/pickups/{pickup_id}/approve`
- `PUT /api/v1/admin/pickups/{pickup_id}/assign-agent`
- `PUT /api/v1/admin/items/{item_id}/assign-center`

### Agent
- `GET /api/v1/agent/pickups`
- `PUT /api/v1/agent/pickups/{pickup_id}/status`

### Processing
- `POST /api/v1/processing`
- `PUT /api/v1/processing/{processing_id}`
- `GET /api/v1/processing/item/{item_id}`

### Rewards
- `GET /api/v1/rewards/my-rewards`
- `GET /api/v1/rewards/my-points`
- `GET /api/v1/certificates/my-certificates`

## Example Workflow
1. User registers and logs in
2. User adds an e-waste item
3. User creates a pickup request
4. Admin reviews and approves the request
5. Admin assigns a pickup agent
6. Pickup agent collects the item
7. Admin assigns the item to a repair or recycling center
8. Center updates processing progress
9. User receives points and final status update

## Security Notes
- Store passwords using bcrypt hashing
- Use JWT for stateless authentication
- Restrict endpoints by role
- Never expose sensitive fields in API responses
- Use request validation with Pydantic

## Future Improvements
- QR code tracking
- Email notifications
- PDF certificate generation
- Image upload to cloud storage
- Geo-based nearest center lookup
- Analytics dashboard
- Docker support
- Unit and integration tests

## Author
Developed for the **ReCycleX** e-waste management project using **FastAPI**.
