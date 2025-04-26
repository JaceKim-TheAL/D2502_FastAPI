# controller/users.py

from fastapi import APIRouter

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{user_id}")
def read_user(user_id: int, q1: str = None, ):
    return {"user_id": user_id, "q1": q1, "q2": q2}
