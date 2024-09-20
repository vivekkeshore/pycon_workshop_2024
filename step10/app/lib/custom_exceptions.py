from app.lib.constants import DEFAULT_ERROR_MESSAGE


class CustomBaseException(Exception):
	def __init__(self, msg=DEFAULT_ERROR_MESSAGE):
		# pylint: disable=W0235
		super().__init__(msg)


class DuplicateRecordError(CustomBaseException):
	"""Raise when the record already exists in the database."""
	pass


class RecordNotFoundError(CustomBaseException):
	"""Raise when the record does not exist in the database."""
	pass


class CreateRecordException(CustomBaseException):
	"""Raise when creating the records in database fails."""
	pass


class UpdateRecordException(CreateRecordException):
	"""Raise when updating the records in database fails."""
	pass


class DeleteRecordException(CustomBaseException):
	"""Raise when deleting the records from database fails."""
	pass


class DBFetchFailureException(CustomBaseException):
	"""Raise when fetching the records from database fails."""
	pass


class InvalidDataException(CustomBaseException):
	"""Raise when the data or argument is invalid."""
	pass


class InvalidPasswordException(CustomBaseException):
	"""Raise when the password is invalid."""
	pass
