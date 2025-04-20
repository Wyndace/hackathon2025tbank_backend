from botocore.exceptions import ClientError
from aiobotocore.session import get_session

from core.config import Settings
from core.logger import logger


async def ensure_bucket_exists() -> None:
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=f"http://{Settings.MINIO_HOST}:{Settings.MINIO_PORT}",
        aws_access_key_id=Settings.MINIO_USER,
        aws_secret_access_key=Settings.MINIO_PASSWORD,
        region_name="us-east-1"
    ) as client:
        try:
            await client.head_bucket(Bucket=Settings.BUCKET)
            logger.info(f"Бакет '{Settings.BUCKET}' уже существует.")
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                await client.create_bucket(Bucket=Settings.BUCKET)
                logger.info(f"Бакет '{Settings.BUCKET}' успешно создан.")
            else:
                logger.error(f"Ошибка при проверке бакета: {e}")
                raise

async def upload_to_minio(file_bytes: bytes, object_name: str) -> None:
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=f"http://{Settings.MINIO_HOST}:{Settings.MINIO_PORT}",
        aws_access_key_id=Settings.MINIO_USER,
        aws_secret_access_key=Settings.MINIO_PASSWORD,
    ) as client:
        await client.put_object(
            Bucket=Settings.BUCKET,
            Key=object_name,
            Body=file_bytes
        )
        logger.info(f"Фото {object_name} загружено в MinIO")


async def get_from_minio(object_name: str) -> str:
    session = get_session()
    async with session.create_client(
        "s3",
        endpoint_url=f"http://{Settings.MINIO_HOST}:{Settings.MINIO_PORT}",
        aws_access_key_id=Settings.MINIO_USER,
        aws_secret_access_key=Settings.MINIO_PASSWORD,
    ) as client:
        try:
            response = await client.generate_presigned_url(
                "get_object",
                Params={
                    "Bucket": Settings.BUCKET,
                    "Key": object_name,
                },
                ExpiresIn=1_000_000
            )
            logger.info(f"Ссылка на файл {object_name} успешно сгенерирована")
            return response
        except Exception as e:
            logger.error(f"Ошибка генерации ссылки: {e}")
            raise
