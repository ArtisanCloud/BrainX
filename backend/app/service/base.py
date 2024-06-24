from typing import List, Any, Tuple

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database.base import PER_PAGE
from app.schemas.base import Pagination, ResponsePagination


async def paginate_query(
        db: AsyncSession,
        query: select,
        table: Any,
        pagination: Pagination,
        sort: bool,
) -> Tuple[List[Any] | None, ResponsePagination | None, SQLAlchemyError | None]:
    try:
        # 如果页码小于等于 0 或者为 None，默认设置为 1
        page = pagination.page or 1
        # 如果每页条目数小于等于 0 或者为 None，默认设置为 10
        page_size = pagination.page_size or PER_PAGE

        # 应用分页参数
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        # print(query, offset, page_size)

        # 打印 SQL 查询语句
        # print("SQL Pagination Query:", str(query))

        # 执行查询并获取结果
        result = await db.execute(query)
        items = result.scalars().all()

        # 获取总行数
        result = await db.execute(select(func.count('*')).select_from(table))
        total_rows = result.scalars().one()
        # total_rows = await db.query(func.count('*'))
        # 计算总页数
        total_pages = (total_rows + page_size - 1) // page_size
        # print(total_rows, total_pages)

    except SQLAlchemyError as e:

        return None, None, e

    # 构造 ResponsePagination 对象
    pagination_info = ResponsePagination(
        limit=page_size,
        page=page,
        sort=sort,  # 这里需要根据实际情况设置排序方式
        total_rows=total_rows,
        total_pages=total_pages
    )

    return items, pagination_info, None
