from fastapi import Depends
from sqlalchemy.orm import Session

from app.dependencies.database_dependencies import get_db
from app.repositories.file_repository import FileRepository
from app.services.file_service import FileService


def get_file_repository(
    db: Session = Depends(get_db),
) -> FileRepository:
    return FileRepository(db)


def get_file_service(
    repository: FileRepository = Depends(get_file_repository),
) -> FileService:
    return FileService(repository)