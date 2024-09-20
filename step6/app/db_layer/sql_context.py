from app.models import SessionLocal


class SqlContext:
	def __init__(self):
		self.session = SessionLocal()

	def __enter__(self):
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		self.close()

	def execute(self, query):
		return self.session.execute(query)

	def close(self):
		try:
			self.session.commit()
		except Exception as ex:
			self.session.rollback()
			raise ex
