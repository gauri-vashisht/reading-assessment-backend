from sqlalchemy.orm import Session

from app.exceptions.custom import NotFoundException


class BaseService:

    def __init__(
        self,
        repository,
        resource_name: str,
    ):
        self.repository = repository
        self.resource_name = resource_name

    def get_by_id(
        self,
        db: Session,
        id,
    ):
        obj = self.repository.get_by_id(
            db,
            id,
        )

        if obj is None:
            raise NotFoundException(
                self.resource_name,
            )

        return obj

    def get_all(
        self,
        db: Session,
    ):
        return self.repository.get_all(db)

    def delete(
        self,
        db: Session,
        id,
    ):
        obj = self.get_by_id(
            db,
            id,
        )

        self.repository.delete(
            db,
            obj,
        )