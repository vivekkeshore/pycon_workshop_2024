ORDER_STATUS_PENDING = "Pending"
ORDER_STATUS_COMPLETED = "Completed"
ORDER_STATUS_CANCELLED = "Cancelled"
ORDER_STATUS_REJECTED = "Rejected"
ORDER_STATUS_SHIPPED = "Shipped"
ORDER_STATUS_DELIVERED = "Delivered"
ORDER_STATUS_RETURNED = "Returned"
ORDER_STATUS_CONFIRMED = "Confirmed"

DEFAULT_ERROR_MESSAGE = "An unexpected error has occurred while processing your request."

# JWT utils constants
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours
JWT_ALGORITHM = "HS256"

UUID_REGEX = "[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12}"

CONTENT_TYPE = "content-type"
JSON_MIME_TYPE = "application/json"
JSON_SIZE_LIMIT = 1024 * 1024  # 1 MB

