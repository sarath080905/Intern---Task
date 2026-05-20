# ==============================
# Authentication helpers
# ==============================
# Imports for security, token verification, and database access.
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import crud
import models
from database import get_db
from utils.security import ALGORITHM, SECRET_KEY

# OAuth2 scheme used to parse the Authorization header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> models.User:
    # Raise a reusable exception for invalid or missing tokens.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Load authenticated user from database.
    user = crud.get_user(db, user_id=int(user_id))
    if user is None:
        raise credentials_exception
    return user
