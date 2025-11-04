import bcrypt

def get_hashed_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password=password.encode(), salt=salt)
    return hashed.decode()

def verify_password(password: str, hashed_pass: str) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_pass.encode())
