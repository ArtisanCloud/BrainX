from contextvars import ContextVar

import uuid
from fastapi import Request
from sqlalchemy.orm import Session

from app.models.originaztion.user import User
from app.logger import logger
from app.schemas.tenant.user import UserTokenData, UserSchema, UserStatus
from app.utils.exceptions import AuthException

# we are using context variables to store request level context , as FASTAPI
# does not provide request context out of the box

# context_db_session stores db session created for every request
context_db_session: ContextVar[Session | None] = ContextVar('db_session', default=None)
# context_api_id stores unique id for every request
context_api_id: ContextVar[str | None] = ContextVar('api_id', default=None)
# context_log_meta stores log meta data for every request
context_log_meta: ContextVar[dict] = ContextVar('log_meta', default={})
# context_user_id stores tenant id coming from client for every request
context_user_id: ContextVar[str | None] = ContextVar('user_id', default=None)
# context_actor_user_data stores tenant data coming from token for every request
context_actor_user_data: ContextVar[UserTokenData | None] = ContextVar('actor_user_data', default=None)
# context_set_db_session_rollback stores flag to rollback db session or not
context_set_db_session_rollback: ContextVar[bool] = ContextVar('set_db_session_rollback', default=False)


async def build_request_context(request: Request):
    # set the db-session in context-var so that we don't have to pass this dependency downstream
    # Convert AsyncSession to Session

    context_api_id.set(str(uuid.uuid4()))
    context_user_id.set(request.headers.get('X-User-ID'))
    # fetch the token from context and check if the tenant is active or not
    user_data_from_context: UserTokenData = context_actor_user_data.get()
    if user_data_from_context:
        user: UserSchema = User.get_by_uuid(user_data_from_context.uuid)
        error_message = None
        if not user:
            error_message = "Invalid authentication credentials, tenant not found"
        elif user.role != user_data_from_context.role:
            error_message = "Invalid authentication credentials, tenant role mismatch"
        elif user.status != UserStatus.ACTIVE.value:
            error_message = "Invalid authentication credentials, tenant is not active"
        if error_message:
            raise AuthException(status_code=401, message=error_message)
    context_log_meta.set({'api_id': context_api_id.get(), 'request_id': request.headers.get('X-Request-ID'),
                          'user_id': context_user_id.get(), 'actor': context_actor_user_data.get()})
    logger.info(extra=context_log_meta.get(), msg="REQUEST_INITIATED")

