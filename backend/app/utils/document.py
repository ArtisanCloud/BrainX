import aioftp
import aiohttp
import urllib.parse
import io
import os
import mimetypes
import urllib.parse
import requests
from typing import Tuple, Dict, Any
from ftplib import FTP
from app import settings
from app.logger import logger


def load_document(document_url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        parsed_url = urllib.parse.urlparse(document_url)

        if parsed_url.scheme in ["ftp"]:
            return parse_ftp_document(document_url)
        if parsed_url.scheme in ["http", "https"]:
            return parse_http_document(document_url)
        elif parsed_url.scheme in ["", "file"]:
            return parse_local_document(parsed_url, document_url)
        else:
            return None, ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")

    except Exception as e:
        logger.error(f"Error processing document URL: {str(e)}")
        return None, e


def parse_http_document(url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # 获取文件名
        file_name = os.path.basename(urllib.parse.urlparse(url).path) or "downloaded_file"
        mime_type = response.headers.get("Content-Type", "application/octet-stream")

        # 读取二进制内容
        content = io.BytesIO(response.content)

        return {
            "content": content,
            "mime_type": mime_type,
            "is_url": True,
            "file_name": file_name,
        }, None

    except Exception as e:
        return None, e


def parse_ftp_document(url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        parsed_url = urllib.parse.urlparse(url)
        ftp_host = parsed_url.hostname
        ftp_port = parsed_url.port or 21
        ftp_user = parsed_url.username or settings.apqp.ftp.username
        ftp_pass = parsed_url.password or settings.apqp.ftp.password

        # 获取文件路径
        file_path = parsed_url.path.lstrip("/")
        file_name = os.path.basename(file_path) or "downloaded_file"

        # 连接 FTP 服务器
        ftp = FTP()
        ftp.connect(ftp_host, ftp_port)
        ftp.login(ftp_user, ftp_pass)

        # 读取文件内容
        content = io.BytesIO()
        ftp.retrbinary(f"RETR {file_path}", content.write)
        ftp.quit()

        content.seek(0)  # 重要：重置文件指针到开头
        mime_type, _ = mimetypes.guess_type(file_name)
        if mime_type is None:
            mime_type = "application/octet-stream"  # 如果无法识别 MIME 类型，使用默认值

        return {
            "content": content,
            "mime_type": mime_type,
            "is_url": True,
            "file_name": file_name,
        }, None

    except Exception as e:
        return None, e


def parse_local_document(
        parsed_url: urllib.parse.ParseResult, document_url: str
) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        file_path = parsed_url.path if parsed_url.scheme == "file" else document_url
        if not os.path.exists(file_path):
            return None, FileNotFoundError(f"CSR Load File not found: {file_path}")

        # 获取文件名
        file_name = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        # 读取文件内容
        with open(file_path, "rb") as f:
            content = io.BytesIO(f.read())

        return {
            "content": content,
            "mime_type": mime_type,
            "is_url": False,
            "file_name": file_name,
        }, None
    except Exception as e:
        return None, e


async def a_load_document(document_url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        parsed_url = urllib.parse.urlparse(document_url)
        # logger.info(f"load remote document parsed_url: {parsed_url}")

        if parsed_url.scheme in ["ftp"]:
            return await a_parse_ftp_document(document_url)
        if parsed_url.scheme in ["http", "https"]:
            return await a_parse_http_document(document_url)
        elif parsed_url.scheme in ["", "file"]:
            return await a_parse_local_document(parsed_url, document_url)
        else:
            return None, ValueError(f"Unsupported URL scheme: {parsed_url.scheme}")

    except Exception as e:
        logger.error(f"Error processing document URL: {str(e)}")
        return None, e


async def a_parse_http_document(url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()

                # 从 URL 中获取文件名
                file_name = os.path.basename(urllib.parse.urlparse(url).path) or "downloaded_file"

                mime_type = response.content_type or "application/octet-stream"

                # 读取二进制内容
                content = io.BytesIO(await response.read())

                return {
                    "content": content,
                    "mime_type": mime_type,
                    "is_url": True,
                    "file_name": file_name,
                }, None

    except Exception as e:
        return None, e


async def a_parse_ftp_document(url: str) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        parsed_url = urllib.parse.urlparse(url)
        ftp_host = parsed_url.hostname
        ftp_port = parsed_url.port or 21
        ftp_user = parsed_url.username or settings.apqp.ftp.username
        ftp_pass = parsed_url.password or settings.apqp.ftp.password
        # logger.info(f"ftp_host: {ftp_host}, ftp_port: {ftp_port}, ftp_user: {ftp_user})

        # 获取文件路径
        file_path = parsed_url.path.lstrip("/")
        file_name = os.path.basename(file_path) or "downloaded_file"

        # 连接 FTP 并下载文件
        async with aioftp.Client.context(
                ftp_host, port=ftp_port,
                user=ftp_user, password=ftp_pass,
        ) as client:
            async with client.download_stream(file_path) as stream:
                content = io.BytesIO(await stream.read())

        return {
            "content": content,
            "mime_type": "application/octet-stream",
            "is_url": True,
            "file_name": file_name,
        }, None
    except Exception as e:
        return None, e


async def a_parse_local_document(
        parsed_url: urllib.parse.ParseResult, document_url: str
) -> Tuple[Dict[str, Any] | None, Exception | None]:
    try:
        file_path = parsed_url.path if parsed_url.scheme == "file" else document_url
        if not os.path.exists(file_path):
            return None, FileNotFoundError(f"CSR Load File not found: {file_path}")

        # 获取文件名
        file_name = os.path.basename(file_path)
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = "application/octet-stream"

        content = io.BytesIO(open(file_path, "rb").read())
        return {
            "content": content,
            "mime_type": mime_type,
            "is_url": False,
            "file_name": file_name,
        }, None
    except Exception as e:
        return None, e
