from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

password = "Password123"

hashed = hash_password(password)

print("Password Hash")
print(hashed)

print()

print("Verify Password")
print(verify_password(password, hashed))

print()

token = create_access_token(
    subject="teacher@gmail.com",
    role="teacher",
)

print("JWT Token")
print(token)

print()

print("Decoded Token")
print(decode_access_token(token))