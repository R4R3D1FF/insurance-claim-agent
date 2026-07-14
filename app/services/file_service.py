from app.repositories.file_repository import FileRepository


class FileService:
    def __init__(self, repository: FileRepository):
        self.repository = repository

    def get_path(self, file_id: int) -> str:
        file = self.repository.get(file_id)

        if file is None:
            return None
        return file.filesystem_path
    
    def create_file(self, filesystem_path: str) -> int:
        file = self.repository.create(filesystem_path)
        return file
    
    def delete_file(self, file_id: int) -> None:
        self.repository.delete(file_id)