from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import httpx
from app.config import settings

security = HTTPBearer()

async def verify_deafauth_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> dict:
    """Verify DeafAUTH JWT token"""
    token = credentials.credentials
    
    try:
        # Decode JWT
        payload = jwt.decode(
            token,
            settings.DEAFAUTH_PUBLIC_KEY,
            algorithms=["RS256"]
        )
        
        # Validate with DeafAUTH service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                settings.DEAFAUTH_VERIFY_URL,
                json={"token": token},
                timeout=5.0
            )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token validation failed"
                )
        
        return payload
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )
