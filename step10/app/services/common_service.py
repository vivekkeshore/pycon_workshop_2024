from typing import Union, List
from uuid import UUID

from fastapi.logger import logger

from app.db_layer.base_repo import BaseRepo
from app.lib.custom_exceptions import DBFetchFailureException, RecordNotFoundError
from app.lib.custom_exceptions import InvalidDataException
from app.lib.singleton import Singleton
from app.models.base_model import BaseModel


class CommonService(metaclass=Singleton):
    @staticmethod
    def get_record_by_id(repo: BaseRepo, record_id: (str, UUID)) -> BaseModel:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the get_record_by_id service. Model - {model_name}. "
            f"{model_name} ID - {record_id}"
        )
        try:
            record = repo.get_by_id(record_id)
        except Exception as ex:
            error_msg = f"Unable to fetch {model_name} details. {model_name} ID - {record_id}"
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise DBFetchFailureException(error_msg)

        if not record:
            error_msg = f"No {model_name} exists with ID - {record_id}"
            logger.error(error_msg)
            raise RecordNotFoundError(error_msg)

        logger.info(f"Succesfully fetched {model_name} with ID - {record_id}")
        return record

    @staticmethod
    def get_record_by_name(repo: BaseRepo, name: str) -> BaseModel:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the get_record_by_name service. Model - {model_name}. "
            f"Name - {name}"
        )
        try:
            records = repo.get_by_col(col="name", value=name)
        except Exception as ex:
            error_msg = f"Unable to fetch {model_name} details. {model_name} name - {name}"
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise DBFetchFailureException(error_msg)

        if not records:
            error_msg = f"No {model_name} exists with name - {name}"
            logger.error(error_msg)
            raise RecordNotFoundError(error_msg)

        logger.info(f"Succesfully fetched {model_name} with name - {name}")
        return records[0] if len(records) == 1 else records

    @staticmethod
    def get_record_by_col(
        repo: BaseRepo, col: str, value: (str, int, float, UUID)
    ) -> Union[BaseModel, List[BaseModel]]:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the get_record_by_col service. Model - {model_name}. "
            f"Col - {col} | Value - {value}"
        )
        try:
            records = repo.get_by_col(col, value)
        except Exception as ex:
            error_msg = f"Unable to fetch {model_name} details. {col} - {value}"
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise DBFetchFailureException(error_msg)

        if not records:
            error_msg = f"No {model_name} exists with {col} - {value}"
            logger.error(error_msg)
            raise RecordNotFoundError(error_msg)

        return records[0] if len(records) == 1 else records

    @staticmethod
    def search_records(repo: BaseRepo, query_params) -> [BaseModel]:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the search_records service. Model - {model_name}. "
            f"Col - {query_params.col} | Value - {query_params.value}"
        )

        if not hasattr(repo.model, query_params.col):
            error_msg = f"Invalid search attribute - {model_name} doesn't have {query_params.col} attribute."
            logger.error(error_msg)
            raise InvalidDataException(error_msg)

        try:
            records = repo.get_all(query_params, ilike=True)
        except Exception as ex:
            error_msg = (
                f"Unable to fetch {model_name} details."
                f"Col - {query_params.col} | Value - {query_params.value}"
            )
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise DBFetchFailureException(error_msg)

        return records

    @staticmethod
    def get_all_records(repo: BaseRepo, query_params) -> [BaseModel]:
        model_name = repo.model.__name__
        is_active_filter = f"| {query_params.is_active}" if hasattr(query_params, "is_active") else ""
        logger.info(
            f"Calling the get_all_records service. Model - {model_name}. "
            f"Page - {query_params.page} | Per Page - {query_params.per_page}"
            f"Count - {query_params.count}{is_active_filter}"
        )
        try:
            records = repo.get_all(query_params)
        except Exception as ex:
            error_msg = f"Unable to fetch {model_name} details."
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise DBFetchFailureException(error_msg)

        return records

    @staticmethod
    def activate_record(repo: BaseRepo, record_id: (str, UUID)) -> BaseModel:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the activate_record service. Model - {model_name}. "
            f"{model_name} ID - {record_id}"
        )
        record = CommonService.get_record_by_id(repo, record_id)
        if record.is_active:
            error_msg = f"{model_name} record is already active. {model_name} ID - {record_id}"
            logger.error(error_msg)
            raise InvalidDataException(error_msg)

        try:
            record = repo.activate_deactivate_record(record, is_active=True)
        except Exception as ex:
            error_msg = (
                f"Unexpected error has occurred while activating the {model_name} record. "
                f"{model_name} ID - {record_id}"
            )
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise RecordNotFoundError(error_msg)

        return record

    @staticmethod
    def deactivate_record(repo: BaseRepo, record_id: (str, UUID)) -> BaseModel:
        model_name = repo.model.__name__
        logger.info(
            f"Calling the deactivate_record service. Model - {model_name}. "
            f"{model_name} ID - {record_id}"
        )
        record = CommonService.get_record_by_id(repo, record_id)
        if not record.is_active:
            error_msg = f"{model_name} record is already inactive. {model_name} ID - {record_id}"
            logger.error(error_msg)
            raise InvalidDataException(error_msg)

        try:
            record = repo.activate_deactivate_record(record, is_active=False)
        except Exception as ex:
            error_msg = (
                f"Unexpected error has occurred while deactivating the {model_name} record. "
                f"{model_name} ID - {record_id}"
            )
            logger.error(f"{error_msg} - {ex}", exc_info=True)
            raise RecordNotFoundError(error_msg)

        return record
