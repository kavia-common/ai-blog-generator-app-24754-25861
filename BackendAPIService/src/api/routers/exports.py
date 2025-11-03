from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.core.database import get_db
from src.api.core.security import get_current_user
from src.api.models import ExportRecord, Post, User
from src.api.schemas import ExportResponse

router = APIRouter(prefix="/exports", tags=["Exports"])


def ensure_owner(post: Post, user: User):
    if post.owner_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized for this post")


def to_markdown(title: str, content: str) -> str:
    if content.strip().lower().startswith("#"):
        return content
    return f"# {title}\n\n{content}"


def to_html(title: str, content: str) -> str:
    # Simple conversion: wrap in basic HTML structure
    body = content
    if not content.strip().lower().startswith("<"):
        body = f"<h1>{title}</h1>\n<p>{content.replace('\\n', '<br/>')}</p>"
    return f"<!doctype html><html><head><meta charset='utf-8'><title>{title}</title></head><body>{body}</body></html>"


@router.get("/{post_id}/html", response_model=ExportResponse, summary="Export post as HTML")
def export_html(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)

    content = to_html(post.title, post.content)
    rec = ExportRecord(post_id=post.id, export_type="html", file_path=None)
    db.add(rec)
    db.commit()

    return ExportResponse(export_type="html", content=content)


@router.get("/{post_id}/markdown", response_model=ExportResponse, summary="Export post as Markdown")
def export_markdown(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)

    content = to_markdown(post.title, post.content)
    rec = ExportRecord(post_id=post.id, export_type="markdown", file_path=None)
    db.add(rec)
    db.commit()

    return ExportResponse(export_type="markdown", content=content)


@router.get("/{post_id}/pdf", response_model=ExportResponse, summary="Export post as PDF (placeholder)")
def export_pdf(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)

    note = "PDF export engine is not configured. This is a placeholder response."
    rec = ExportRecord(post_id=post.id, export_type="pdf", file_path=None)
    db.add(rec)
    db.commit()

    return ExportResponse(export_type="pdf", content="", note=note)
