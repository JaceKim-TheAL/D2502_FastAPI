# controller/admins.py

from fastapi import APIRouter
from model import pgsql_test

router = APIRouter(
    prefix="/admins",
    tags=["admins"],
    responses={404: {"description": "Not found"}},
)

@router.get("/list")
def list_admin():
    """
    List all admins from the database.
    """
    results = pgsql_test.list_admin()
    # return {"user_id": user_id}
    return results



