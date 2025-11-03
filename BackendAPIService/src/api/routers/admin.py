from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.api.core.database import get_db
from src.api.core.security import get_current_admin
from src.api.models import ExportRecord, Post, PostVersion, User

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/stats", summary="Admin statistics", description="Get aggregate statistics for the system.")
def stats(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    users = db.query(func.count(User.id)).scalar() or 0
    posts = db.query(func.count(Post.id)).scalar() or 0
    versions = db.query(func.count(PostVersion.id)).scalar() or 0
    exports = db.query(func.count(ExportRecord.id)).scalar() or 0
    return {"users": users, "posts": posts, "versions": versions, "exports": exports}
