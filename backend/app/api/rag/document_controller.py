import http
from sqlalchemy.exc import SQLAlchemyError

from app.database.base import MAX_PER_PAGE, PAGE, PER_PAGE
from app.logger import logger

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from starlette.requests import Request

from app.api.middleware.auth import get_session_user
from app.database.deps import get_db_session
from app.models import User

from app.schemas.base import Pagination, ResponseSchema
from app.schemas.rag.document import ResponseGetDocumentList, RequestCreateDocument, make_document, \
    RequestPatchDocument, \
    ResponseCreateDocument, ResponsePatchDocument, ResponseDeleteDocument, ResponseGetDocument, \
    RequestAddDocumentContent, ResponseAddDocumentContent, RequestReProcessDocuments, ResponseReProcessDocuments
from app.service.rag.document.add_document_content import add_document_content
from app.service.rag.document.create import create_document
from app.service.rag.document.list import get_document_list, get_document_list_by_documents
from app.service.rag.document.get import get_document_by_uuid
from app.service.rag.document.patch import patch_document
from app.service.rag.document.delete import soft_delete_document

from app.service.task.rag.indexing import process_documents

router = APIRouter()


@router.get("/list")
async def api_get_document_list(
        request: Request,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session),
) -> ResponseGetDocumentList | ResponseSchema:
    # 获取页码和每页条目数，如果参数不存在则默认为1和10
    page = int(request.query_params.get("page", PAGE))
    page_size = int(request.query_params.get("page_size", PER_PAGE))
    dataset_uuid = request.query_params.get("dataset_uuid", '')

    p = Pagination(page=page, page_size=page_size)

    if dataset_uuid == "":
        return ResponseSchema(error=str("lack of dataset_uuid"), status_code=http.HTTPStatus.BAD_REQUEST)

    try:
        documents, pagination, exception = await get_document_list(db, session_user.uuid, dataset_uuid, p)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetDocumentList(data=documents, pagination=pagination)

    return res


@router.get("/{document_uuid}")
async def api_get_document_by_uuid(
        document_uuid: str,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)
):
    try:
        document, exception = await get_document_by_uuid(db, session_user, document_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseGetDocument(data=document)

    return res


@router.post("/create")
async def api_create_document(
        data: RequestCreateDocument,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)):
    try:

        document = make_document(data)
        document.tenant_uuid = str(session_user.tenant_owner_uuid)
        document.created_user_by = str(session_user.uuid)
        # print(document)
        document, exception = await create_document(db, document)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseCreateDocument(document=document)

    return res


@router.patch("/patch/{document_uuid}")
async def api_patch_document(
        document_uuid: str,  # 接收路径参数 document_uuid
        data: RequestPatchDocument,
        db: AsyncSession = Depends(get_db_session)):
    try:

        update_data = data.dict(exclude_unset=True)
        # print(document_uuid, update_data)

        document, exception = await patch_document(db, document_uuid, update_data)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponsePatchDocument(document=document)

    return res


@router.delete("/delete/{document_uuid}")
async def api_delete_document(
        document_uuid: str,  # 接收路径参数 document_uuid
        db: AsyncSession = Depends(get_db_session)):
    try:
        user_id = 1
        result, exception = await soft_delete_document(db, user_id, document_uuid)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

    except Exception as e:
        return ResponseSchema(error=str(e), status_code=http.HTTPStatus.BAD_REQUEST)

    res = ResponseDeleteDocument(result=result)

    return res


@router.post("/add-content")
async def api_add_document_content(
        data: RequestAddDocumentContent,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)):
    try:
        # print(data)
        documents, exception = await add_document_content(db, session_user, data)
        if exception is not None:
            if isinstance(exception, SQLAlchemyError):
                logger.error(exception)
                raise Exception("database query: pls check log")
            raise exception

        # 如果保存dataset和documents 准备数据信息成功
        # 则开始开启后台的worker，做Extractor和Indexing的工作
        document_dict_list = [doc.dict() for doc in documents]
        task = process_documents.apply_async(args=(data.dataset_uuid, document_dict_list,))


    except Exception as e:
        return ResponseSchema(
            error=str(e),
            status_code=http.HTTPStatus.BAD_REQUEST,
        )

    res = ResponseAddDocumentContent(data=documents, task_id=task.id)

    return res


@router.post("/re-process-documents")
async def api_re_process_documents(
        data: RequestReProcessDocuments,
        session_user: User = Depends(get_session_user),
        db: AsyncSession = Depends(get_db_session)):
    try:
        # print(data)
        # 获取用户的documents
        documents, pg, exception = await get_document_list_by_documents(
            db,
            session_user.uuid, data.document_uuids,
            Pagination(page=PAGE, page_size=MAX_PER_PAGE))
        # print(documents)

        # 如果保存dataset和documents 准备数据信息成功
        # 则开始开启后台的worker，做Extractor和Indexing的工作
        document_dict_list = [doc.dict() for doc in documents]
        # print(document_dict_list)
        task = process_documents.apply_async(args=(data.dataset_uuid, document_dict_list,))


    except Exception as e:
        return ResponseSchema(
            error=str(e),
            status_code=http.HTTPStatus.BAD_REQUEST,
        )

    res = ResponseReProcessDocuments(task_id=task.id)

    return res
