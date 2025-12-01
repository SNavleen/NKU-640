# Local Validation Checklist

Complete these steps to validate the application before AWS deployment.

---

## ✅ Pre-Deployment Validation

### 1. Environment Setup

```bash
cd /Users/navi/Documents/NKU/640/NKU-640/homework4/python-version

# Verify uv is installed
uv --version

# Install dependencies
uv sync

# Copy environment file
cp .env.example .env
```

### 2. Start Services

```bash
# Option A: Docker (Recommended)
docker-compose up -d

# Option B: Local development
./scripts/run.sh
```

### 3. Health Check

```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Expected: Status 200 with "healthy" status
```

### 4. API Documentation

Visit http://localhost:8000/docs

✅ Verify:
- Swagger UI loads
- All 14 endpoints visible
- Can execute test requests

### 5. Authentication Flow

```bash
# Sign up
SIGNUP=$(curl -s -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"password123"}')

# Extract token
TOKEN=$(echo $SIGNUP | jq -r '.token')
echo "Token: $TOKEN"

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"password123"}'

# Get profile (protected endpoint)
curl http://localhost:8000/api/v1/users/profile \
  -H "Authorization: Bearer $TOKEN"

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer $TOKEN"
```

✅ Verify:
- [ ] Signup returns token and user
- [ ] Login works with correct credentials
- [ ] Login fails with wrong password (401)
- [ ] Profile requires valid token
- [ ] Logout blacklists token
- [ ] Blacklisted token cannot access profile

### 6. List CRUD Operations

```bash
# Create list
LIST=$(curl -s -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name":"Test List","description":"Testing"}')

LIST_ID=$(echo $LIST | jq -r '.id')

# Get all lists
curl http://localhost:8000/api/v1/lists

# Get specific list
curl http://localhost:8000/api/v1/lists/$LIST_ID

# Update list
curl -X PATCH http://localhost:8000/api/v1/lists/$LIST_ID \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated List"}'

# Delete list
curl -X DELETE http://localhost:8000/api/v1/lists/$LIST_ID
```

✅ Verify:
- [ ] List creation returns 201
- [ ] List has valid UUID
- [ ] Get all lists returns array
- [ ] Get specific list returns correct data
- [ ] Update works (200 response)
- [ ] Delete works (204 response)
- [ ] Deleted list returns 404

### 7. Task CRUD Operations

```bash
# Create list first
LIST=$(curl -s -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name":"Todo List"}')

LIST_ID=$(echo $LIST | jq -r '.id')

# Create task
TASK=$(curl -s -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","priority":"high","categories":["groceries"]}')

TASK_ID=$(echo $TASK | jq -r '.id')

# Get tasks in list
curl http://localhost:8000/api/v1/lists/$LIST_ID/tasks

# Get specific task
curl http://localhost:8000/api/v1/tasks/$TASK_ID

# Update task (mark completed)
curl -X PATCH http://localhost:8000/api/v1/tasks/$TASK_ID \
  -H "Content-Type: application/json" \
  -d '{"completed":true}'

# Delete task
curl -X DELETE http://localhost:8000/api/v1/tasks/$TASK_ID
```

✅ Verify:
- [ ] Task creation returns 201
- [ ] Task has priority field
- [ ] Task has categories array
- [ ] Get tasks returns array
- [ ] Update changes fields
- [ ] Delete works (204 response)

### 8. Cascade Delete

```bash
# Create list with tasks
LIST=$(curl -s -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"name":"Cascade Test"}')

LIST_ID=$(echo $LIST | jq -r '.id')

# Create multiple tasks
TASK1=$(curl -s -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Task 1"}')

TASK2=$(curl -s -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Task 2"}')

TASK1_ID=$(echo $TASK1 | jq -r '.id')

# Delete list
curl -X DELETE http://localhost:8000/api/v1/lists/$LIST_ID

# Verify task is also deleted
curl http://localhost:8000/api/v1/tasks/$TASK1_ID
# Should return 404
```

✅ Verify:
- [ ] Deleting list cascades to tasks
- [ ] Tasks return 404 after list deletion

### 9. Validation Tests

```bash
# Test invalid email
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"invalid","password":"password123"}'
# Expected: 422

# Test short password
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"test","email":"test@example.com","password":"short"}'
# Expected: 422

# Test invalid UUID
curl http://localhost:8000/api/v1/lists/invalid-uuid
# Expected: 400

# Test missing required field
curl -X POST http://localhost:8000/api/v1/lists \
  -H "Content-Type: application/json" \
  -d '{"description":"No name"}'
# Expected: 422

# Test invalid priority
curl -X POST http://localhost:8000/api/v1/lists/$LIST_ID/tasks \
  -H "Content-Type: application/json" \
  -d '{"title":"Task","priority":"urgent"}'
# Expected: 422
```

✅ Verify:
- [ ] Email validation works
- [ ] Password length validated
- [ ] UUID format validated
- [ ] Required fields enforced
- [ ] Enum values validated

### 10. Run Test Suite

```bash
# Run all tests
uv run pytest -v

# Run with coverage
uv run pytest --cov=app --cov-report=term-missing

# Run specific test categories
uv run pytest tests/test_auth.py -v
uv run pytest tests/test_lists.py -v
uv run pytest tests/test_tasks.py -v
```

✅ Verify:
- [ ] All tests pass
- [ ] Coverage > 80%
- [ ] No errors or warnings

### 11. Database Verification

```bash
# Access database
docker exec -it todo_postgres psql -U todo_user -d todo_db

# Check tables
\dt

# Should show: users, lists, tasks, token_blacklist

# Query data
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM lists;
SELECT COUNT(*) FROM tasks;
SELECT COUNT(*) FROM token_blacklist;

# Exit
\q
```

✅ Verify:
- [ ] All tables created
- [ ] Data persists correctly
- [ ] Foreign keys work

### 12. Performance Check

```bash
# Multiple requests
for i in {1..10}; do
  curl -s http://localhost:8000/api/v1/health > /dev/null
done

# Check response times in logs
docker-compose logs app | grep "Time:"
```

✅ Verify:
- [ ] Response times < 100ms
- [ ] No errors in logs
- [ ] Memory usage stable

---

## 📋 Final Checklist

Before AWS deployment, confirm:

- [ ] All health checks pass
- [ ] Authentication flow works end-to-end
- [ ] All CRUD operations functional
- [ ] Cascade delete works
- [ ] Validation catches errors
- [ ] All tests pass (50+ tests)
- [ ] Database persists data correctly
- [ ] No errors in application logs
- [ ] API documentation accessible
- [ ] Docker containers stable

---

## 🚀 Ready for AWS Deployment

Once all checks pass:

```bash
# Deploy to AWS EC2
./scripts/deploy-ec2.sh
```

See deployment guide in README.md for details.

---

## 🐛 Troubleshooting

### Issue: Port already in use
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Issue: Database connection failed
```bash
# Restart database
docker-compose restart db

# Check logs
docker-compose logs db
```

### Issue: Tests failing
```bash
# Clear cache
uv run pytest --cache-clear

# Reinstall dependencies
uv sync --force
```

---

**Status:** Ready for validation ✅
**Next Step:** Run through checklist, then deploy to AWS
