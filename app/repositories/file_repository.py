from sqlalchemy.orm import Session

from app.models.file import File


class FileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, file_id: int) -> File | None:
        return self.db.get(File, file_id)
    
    def create(self, filesystem_path: str) -> File:
        file = File(filesystem_path=filesystem_path)

        self.db.add(file)
        self.db.commit()
        self.db.refresh(file)

        return file
    
    def delete(self, file_id: int):
        file = self.get(file_id)

        if file is None:
            return
        
        self.db.delete(file)
        self.db.commit()