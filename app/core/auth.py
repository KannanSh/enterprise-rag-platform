from dataclasses import dataclass
from fastapi import Header, HTTPException, status

@dataclass(frozen=True)
class Principal:
    user_id: str
    role: str

DEMO_KEYS = {
    "demo-admin": Principal("demo-admin", "admin"),
    "demo-analyst": Principal("demo-analyst", "analyst"),
    "demo-viewer": Principal("demo-viewer", "viewer"),
}

ROLE_ORDER = {"viewer": 1, "analyst": 2, "admin": 3}

def get_principal(x_api_key: str | None = Header(default=None)) -> Principal:
    if x_api_key not in DEMO_KEYS:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid API key")
    return DEMO_KEYS[x_api_key]

def require_role(min_role: str):
    def dependency(principal: Principal = __import__("fastapi").Depends(get_principal)):
        if ROLE_ORDER[principal.role] < ROLE_ORDER[min_role]:
            raise HTTPException(status_code=403, detail="Insufficient role")
        return principal
    return dependency
