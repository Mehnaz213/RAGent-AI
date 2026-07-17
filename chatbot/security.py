# Import datetime utilities
from datetime import datetime, timedelta
# Import JWT functions
from jose import JWTError, jwt
# Import password hashing
from passlib.context import CryptContext
from jose import JWTError, ExpiredSignatureError

print("security.py loaded")
# Secret key used to sign JWT tokens
SECRET_KEY = "your_super_secret_key_change_this"
# JWT algorithm
ALGORITHM = "HS256"
# Token expiry time (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

# Password hashing configuration
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
# Convert plain password into hashed password
def hash_password(password: str):
    return pwd_context.hash(password)

# Verify entered password with stored hashed password
def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# Generate JWT Access Token
def create_access_token(data: dict):
    # Copy user data
    to_encode = data.copy()
    # Calculate expiry time
    expire = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    # Add expiry into token
    to_encode.update(
        {
            "exp": expire
        }
    )
    # Create JWT token
    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

# Decode JWT token
def verify_access_token(token: str):

    print("verify_access_token() called")

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        print("Decoded JWT:", payload)

        return payload

    except ExpiredSignatureError as e:
        print("Expired Token:", repr(e))
        return None

    except JWTError as e:
        print("JWT Error:", repr(e))
        return None

    except Exception as e:
        print("Unknown Error:", repr(e))
        return None