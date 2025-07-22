from fastapi import Depends, HTTPException, status

from app.db.models.user import User
from app.services.auth import get_current_user

def get_current_admin_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
