# Safety Rules and Security Best Practices

## Overview

This document outlines the security measures, safety rules, and best practices implemented in the TODO REST API to ensure data protection, prevent common vulnerabilities, and maintain system integrity.

---

## Table of Contents

1. [Authentication & Authorization](#authentication--authorization)
2. [Input Validation](#input-validation)
3. [Database Security](#database-security)
4. [Password Security](#password-security)
5. [Token Management](#token-management)
6. [API Security](#api-security)
7. [Environment Configuration](#environment-configuration)
8. [Error Handling](#error-handling)
9. [Rate Limiting](#rate-limiting)
10. [Deployment Security](#deployment-security)

---

## Authentication & Authorization

### JWT Token Security

**Implementation:**
- JWT tokens are signed using HS256 algorithm with a secret key
- Tokens include user ID (`sub` claim), issuance time (`iat`), and expiration (`exp`)
- Tokens expire after 1 hour (configurable)
- Blacklist mechanism prevents token reuse after logout

**Best Practices:**
- Always use HTTPS in production to prevent token interception
- Store JWT_SECRET securely (never commit to version control)
- Use strong, random secret keys (minimum 32 characters)
- Implement token refresh mechanism for long-lived sessions
- Monitor failed authentication attempts

**Code Example:**
```python
# JWT token creation with expiration
def create_access_token(data: Dict[str, str]):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRY)
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    return jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
```

### Token Blacklisting

**Why It's Needed:**
Without blacklisting, a stolen JWT token remains valid until expiration (up to 1 hour), even after the user logs out.

**How It Works:**
1. User logs out → Token added to blacklist database
2. Every protected endpoint checks if token is blacklisted
3. Expired tokens are automatically cleaned up
4. Blacklisted tokens return 401 Unauthorized

**Database Table:**
```sql
CREATE TABLE token_blacklist (
    id TEXT PRIMARY KEY,
    token TEXT UNIQUE NOT NULL,
    user_id TEXT NOT NULL,
    blacklisted_at TIMESTAMP NOT NULL,
    expires_at TIMESTAMP NOT NULL
);
```

**Security Benefits:**
- Immediate token invalidation on logout
- Prevents stolen tokens from being used
- Enables "logout all devices" functionality
- Allows admin to blacklist compromised tokens

---

## Input Validation

### Validation Layers

**1. Pydantic Schema Validation:**
- Automatic type checking
- Field length limits
- Email format validation
- Custom validators for business rules

**Example:**
```python
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)

    @validator('username')
    def username_alphanumeric(cls, v):
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username must be alphanumeric')
        return v.strip()
```

**2. UUID Validation:**
```python
def validate_uuid(uuid_string: str, field_name: str = "ID") -> str:
    try:
        uuid_obj = uuid.UUID(uuid_string, version=4)
        return str(uuid_obj)
    except (ValueError, AttributeError):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid {field_name} format. Must be a valid UUID v4."
        )
```

**3. String Sanitization:**
- Trim whitespace from all inputs
- Reject empty or whitespace-only strings for required fields
- Enforce maximum lengths to prevent buffer overflow

### Validation Rules

**User Data:**
- Username: 3-50 characters, alphanumeric (underscores/hyphens allowed)
- Email: Valid email format, unique
- Password: Minimum 8 characters

**List Data:**
- Name: Required, 1-255 characters, not only whitespace
- Description: Optional, max 1000 characters

**Task Data:**
- Title: Required, 1-255 characters, not only whitespace
- Description: Optional, max 2000 characters
- Priority: Enum ('low', 'medium', 'high')
- Categories: Array, max 10 items, each max 50 characters
- Due Date: ISO 8601 format

---

## Database Security

### SQL Injection Prevention

**Primary Defense: SQLAlchemy ORM**

The application uses SQLAlchemy ORM exclusively, which automatically uses parameterized queries to prevent SQL injection.

**Safe Example:**
```python
# SQLAlchemy automatically parameterizes this query
user = db.query(User).filter(User.username == username).first()
```

**NEVER DO THIS:**
```python
# UNSAFE: String concatenation (SQL injection vulnerable)
query = f"SELECT * FROM users WHERE username = '{username}'"
```

**Additional Protections:**
- No raw SQL queries
- All user inputs validated before database operations
- Database user has minimal required permissions
- Foreign key constraints enforced

### Transaction Safety

**Implementation:**
```python
try:
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
except IntegrityError:
    db.rollback()
    raise HTTPException(status_code=409, detail="Conflict")
```

**Best Practices:**
- Use transactions for multi-table operations
- Implement proper rollback on errors
- Use database constraints (UNIQUE, FOREIGN KEY, NOT NULL)
- Enable cascade deletes where appropriate

---

## Password Security

### Bcrypt Hashing

**Implementation:**
```python
from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=12  # Cost factor
)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

**Security Features:**
- Bcrypt with cost factor 12 (recommended by OWASP)
- Automatic salt generation
- Resistant to rainbow table attacks
- Slow hashing makes brute-force attacks impractical

**Best Practices:**
- Never store passwords in plain text
- Never log passwords
- Never return passwords in API responses
- Enforce minimum password length (8 characters)
- Consider password complexity requirements for production

---

## Token Management

### Token Lifecycle

**1. Token Creation (Login/Signup):**
```python
access_token = create_access_token(data={"sub": user.id})
```

**2. Token Validation (Protected Endpoints):**
```python
def get_current_user(credentials: HTTPAuthorizationCredentials, db: Session):
    # 1. Check if blacklisted
    # 2. Verify JWT signature
    # 3. Check expiration
    # 4. Get user from database
```

**3. Token Blacklisting (Logout):**
```python
def blacklist_token(db: Session, token: str, user_id: str, expires_at: datetime):
    # Add to blacklist
    # Clean up expired tokens
```

### Security Considerations

**Token Storage (Client-Side):**
- Store in HTTP-only cookies (prevents XSS)
- Or store in memory (not localStorage - vulnerable to XSS)
- Include token in Authorization header: `Bearer <token>`

**Token Expiration:**
- Default: 1 hour
- Balance security vs user experience
- Shorter expiration = more secure but more frequent re-authentication

**Token Cleanup:**
```python
# Automatic cleanup of expired blacklisted tokens
db.query(TokenBlacklist).filter(
    TokenBlacklist.expires_at < datetime.utcnow()
).delete()
```

---

## API Security

### CORS Configuration

**Nginx Configuration:**
```nginx
add_header 'Access-Control-Allow-Origin' '*' always;
add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, DELETE, OPTIONS' always;
add_header 'Access-Control-Allow-Headers' 'Authorization, Content-Type' always;
```

**Production Recommendations:**
- Replace `*` with specific allowed origins
- Limit allowed methods to only what's needed
- Enable credentials if using cookies
- Implement CSRF protection

### Security Headers

**Implemented in Nginx:**
```nginx
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
```

**What They Do:**
- **X-Frame-Options**: Prevents clickjacking attacks
- **X-Content-Type-Options**: Prevents MIME type sniffing
- **X-XSS-Protection**: Enables browser XSS filter
- **Referrer-Policy**: Controls referrer information

### Content-Type Validation

**FastAPI automatically validates:**
- Request Content-Type must be `application/json` for POST/PATCH
- Response Content-Type is always `application/json`
- Invalid Content-Type returns 415 Unsupported Media Type

---

## Environment Configuration

### Environment Variables

**Required for Production:**
```env
# CRITICAL: Change these in production
JWT_SECRET=your-strong-random-secret-at-least-32-characters-long

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Security
DEBUG_MODE=false
LOG_LEVEL=error

# JWT
JWT_EXPIRY=3600
BCRYPT_ROUNDS=12
```

### Configuration Best Practices

**DO:**
- Use environment variables for all secrets
- Use different secrets for each environment
- Generate random, strong secrets (use `openssl rand -hex 32`)
- Use `.env.example` for documentation, never `.env`
- Add `.env` to `.gitignore`

**DON'T:**
- Commit secrets to version control
- Use default/example secrets in production
- Hardcode credentials in code
- Share secrets via email or chat

### Secret Generation

```bash
# Generate strong JWT secret
openssl rand -hex 32

# Or use Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## Error Handling

### Production Error Responses

**Debug Mode OFF (Production):**
```json
{
  "error": "Internal server error",
  "code": "INTERNAL_ERROR",
  "details": {}
}
```

**Debug Mode ON (Development):**
```json
{
  "error": "Database connection failed",
  "code": "DATABASE_ERROR",
  "details": {
    "exception": "psycopg2.OperationalError",
    "message": "could not connect to server"
  }
}
```

### Logging Best Practices

**DO Log:**
- Request method, path, status code, response time
- Authentication failures (username, not password)
- Authorization failures
- Validation errors
- Server errors with stack traces

**DON'T Log:**
- Passwords (plain or hashed)
- JWT tokens
- Personal identifiable information (PII)
- Credit card numbers
- API keys

**Example:**
```python
# Good
logger.info(f"Login attempt for user: {username}")

# Bad
logger.info(f"Login attempt: {username}:{password}")
```

---

## Rate Limiting

### Nginx Rate Limiting

**Configuration:**
```nginx
limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

location /api/ {
    limit_req zone=api_limit burst=20 nodelay;
}
```

**What This Does:**
- 10 requests per second per IP
- Burst of 20 requests allowed
- Excess requests return 429 Too Many Requests

### Rate Limiting Best Practices

**Recommendations:**
- Lower limits for authentication endpoints (5 req/min)
- Higher limits for read operations
- Use different zones for different endpoints
- Implement distributed rate limiting for multi-server deployments
- Add rate limit headers in responses

---

## Deployment Security

### Production Checklist

**Before Deploying:**
- [ ] Change all default secrets
- [ ] Set `DEBUG_MODE=false`
- [ ] Set `LOG_LEVEL=error`
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Configure firewall rules
- [ ] Set up monitoring and alerts
- [ ] Configure automated backups
- [ ] Review and update dependencies
- [ ] Run security audit

### HTTPS/TLS Configuration

**Why It's Critical:**
- Prevents man-in-the-middle attacks
- Protects JWT tokens in transit
- Encrypts sensitive data
- Required for authentication security

**Nginx SSL Configuration:**
```nginx
server {
    listen 443 ssl http2;
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
}
```

### Database Security

**Production Recommendations:**
- Use strong database passwords
- Restrict database access to application servers only
- Enable SSL/TLS for database connections
- Regular backups with encryption
- Separate database user for application (not root)
- Grant minimal required permissions

### Docker Security

**Best Practices:**
- Use official base images
- Update images regularly
- Don't run as root user
- Use secrets management for sensitive data
- Scan images for vulnerabilities
- Limit container resources

---

## Security Monitoring

### What to Monitor

**Authentication Events:**
- Failed login attempts
- Account creation rate
- Password reset requests
- Token blacklist size

**API Usage:**
- Request rate per endpoint
- Error rate
- Response times
- Unusual patterns

**System Health:**
- Database connections
- Memory usage
- Disk space
- CPU usage

### Alerting

**Set up alerts for:**
- High rate of authentication failures
- Spike in error rates
- Database connection failures
- Low disk space
- High memory usage
- Unusual access patterns

---

## Incident Response

### If Security Breach Suspected

1. **Immediate Actions:**
   - Rotate JWT_SECRET (invalidates all tokens)
   - Force password reset for affected users
   - Review logs for unauthorized access
   - Check for data exfiltration

2. **Investigation:**
   - Identify breach vector
   - Assess data exposure
   - Document timeline
   - Preserve evidence

3. **Remediation:**
   - Patch vulnerabilities
   - Update dependencies
   - Enhance monitoring
   - Implement additional security measures

4. **Communication:**
   - Notify affected users
   - Document lessons learned
   - Update security procedures

---

## Security Testing

### Automated Testing

**Test Coverage:**
- Authentication bypass attempts
- SQL injection attempts (should fail due to ORM)
- XSS attempts (should be sanitized)
- Token reuse after logout
- Invalid UUID handling
- Input validation edge cases

**Run Tests:**
```bash
uv run pytest tests/
```

### Manual Security Testing

**Tools:**
- OWASP ZAP for vulnerability scanning
- Burp Suite for penetration testing
- sqlmap for SQL injection testing
- JWT.io for token inspection

---

## Compliance Considerations

### OWASP Top 10

**Mitigations Implemented:**
1. **Injection**: SQLAlchemy ORM, input validation
2. **Broken Authentication**: JWT with expiration, token blacklisting
3. **Sensitive Data Exposure**: HTTPS, password hashing, no PII in logs
4. **XML External Entities**: Not applicable (JSON only)
5. **Broken Access Control**: JWT-based authorization
6. **Security Misconfiguration**: Environment-based configuration
7. **XSS**: Input sanitization, security headers
8. **Insecure Deserialization**: Not applicable
9. **Using Components with Known Vulnerabilities**: Regular dependency updates
10. **Insufficient Logging**: Comprehensive logging (without sensitive data)

---

## Additional Resources

- [OWASP API Security Top 10](https://owasp.org/www-project-api-security/)
- [JWT Best Practices](https://tools.ietf.org/html/rfc8725)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [SQLAlchemy Security](https://docs.sqlalchemy.org/en/14/faq/security.html)

---

## Updates and Maintenance

**Regular Security Tasks:**
- Update dependencies monthly
- Review logs weekly
- Rotate secrets quarterly
- Security audit annually
- Penetration testing as needed

**Stay Informed:**
- Subscribe to security advisories
- Monitor CVE databases
- Follow security best practices updates
- Join security mailing lists
