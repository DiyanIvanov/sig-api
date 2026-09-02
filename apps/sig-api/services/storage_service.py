import os
import datetime
from azure.storage.blob import BlobServiceClient, ContainerClient, BlobSasPermissions, generate_blob_sas
from io import BytesIO


CONTAINER_NAME = 'invoices'

def upload_pdf(pdf_buffer: BytesIO, file_name: str) -> str:
    connection_string = os.environ['AZURE_STORAGE_CONNECTION_STRING']

    blob_service = BlobServiceClient.from_connection_string(connection_string)

    container = blob_service.get_container_client(CONTAINER_NAME)

    if not container.exists():
        container.create_container()

    blob_client = container.get_blob_client(file_name)

    blob_client.upload_blob(pdf_buffer, overwrite=True)

    return get_blob_sas_url(blob_service, container, file_name)


def get_blob_sas_url(blob_service_client: BlobServiceClient, container: ContainerClient, blob_name: str) -> str:
    account_name = blob_service_client.account_name
    account_key = blob_service_client.credential.account_key
    container_name = container.container_name

    sas_token = generate_blob_sas(
        container_name=container_name,
        blob_name=blob_name,
        account_name=account_name,
        account_key=account_key,
        permission=BlobSasPermissions(read=True),
        expiry=datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    )

    blob_client = container.get_blob_client(blob_name)
    return f"{blob_client.url}?{sas_token}"