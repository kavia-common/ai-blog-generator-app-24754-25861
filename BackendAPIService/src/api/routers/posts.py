from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.api.core.database import get_db
from src.api.core.security import get_current_user
from src.api.models import Post, PostVersion, User
from src.api.schemas import PostCreate, PostOut, PostUpdate, PostVersionOut

router = APIRouter(prefix="/posts", tags=["Posts"])


def ensure_owner(post: Post, user: User):
    if post.owner_id != user.id and not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized for this post")


@router.get("", response_model=List[PostOut], summary="List posts", description="List posts owned by current user.")
def list_posts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    q = db.query(Post)
    if not user.is_admin:
        q = q.filter(Post.owner_id == user.id)
    return q.order_by(Post.updated_at.desc()).all()


@router.post("", response_model=PostOut, summary="Create post", description="Create a new post.")
def create_post(post_in: PostCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = Post(title=post_in.title, content=post_in.content, topic=post_in.topic, owner_id=user.id, version=1)
    db.add(post)
    db.commit()
    db.refresh(post)

    pv = PostVersion(post_id=post.id, version_number=1, content=post.content)
    db.add(pv)
    db.commit()

    return post


@router.get("/{post_id}", response_model=PostOut, summary="Get post", description="Get a single post by ID.")
def get_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)
    return post


@router.put("/{post_id}", response_model=PostOut, summary="Update post (creates new version)", description="Update a post and create a new version.")
def update_post(post_id: int, post_in: PostUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)

    updated = False
    if post_in.title is not None:
        post.title = post_in.title
        updated = True
    if post_in.content is not None:
        post.content = post_in.content
        updated = True
    if post_in.topic is not None:
        post.topic = post_in.topic
        updated = True

    if updated:
        post.version += 1
        post.updated_at = datetime.utcnow()
        db.add(post)
        db.commit()
        db.refresh(post)

        pv = PostVersion(post_id=post.id, version_number=post.version, content=post.content)
        db.add(pv)
        db.commit()

    return post


@router.delete("/{post_id}", summary="Delete post", description="Delete a post and its versions.")
def delete_post(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)
    db.delete(post)
    db.commit()
    return {"status": "deleted"}


@router.get("/{post_id}/versions", response_model=List[PostVersionOut], summary="List post versions", description="List all versions for a post.")
def list_versions(post_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)
    return db.query(PostVersion).filter(PostVersion.post_id == post_id).order_by(PostVersion.version_number.desc()).all()


@router.get("/{post_id}/versions/{version_number}", response_model=PostVersionOut, summary="Get specific version", description="Get a specific version of a post.")
def get_version(post_id: int, version_number: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    ensure_owner(post, user)
    version = db.query(PostVersion).filter(PostVersion.post_id == post_id, PostVersion.version_number == version_number).first()
    if not version:
        raise HTTPException(status_code=404, detail="Version not found")
    return version
