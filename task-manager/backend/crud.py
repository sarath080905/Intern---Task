# ==============================
# Database CRUD operations
# ==============================
# Imports for SQLAlchemy session, models, schemas, and password hashing.
from sqlalchemy.orm import Session

import models
import schemas
from utils.security import hash_password


def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    # Create a new user with hashed password for secure storage.
    db_user = models.User(
        email=user.email,
        hashed_password=hash_password(user.password),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_task(
    db: Session, task: schemas.TaskCreate, owner_id: int
) -> models.Task:
    # Create a new task owned by the current authenticated user.
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed,
        owner_id=owner_id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_task(db: Session, task_id: int, owner_id: int) -> models.Task | None:
    return (
        db.query(models.Task)
        .filter(models.Task.id == task_id, models.Task.owner_id == owner_id)
        .first()
    )


def get_tasks(
    db: Session,
    owner_id: int,
    *,
    completed: bool | None = None,
    page: int = 1,
    limit: int = 10,
) -> tuple[list[models.Task], int]:
    # Query tasks for the current user.
    query = db.query(models.Task).filter(models.Task.owner_id == owner_id)
    if completed is not None:
        query = query.filter(models.Task.completed == completed)

    total = query.count()
    offset = (page - 1) * limit
    items = (
        query.order_by(models.Task.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    return items, total


def update_task(
    db: Session, db_task: models.Task, task: schemas.TaskUpdate
) -> models.Task:
    # Apply only the fields provided in the update request.
    update_data = task.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, db_task: models.Task) -> None:
    db.delete(db_task)
    db.commit()
