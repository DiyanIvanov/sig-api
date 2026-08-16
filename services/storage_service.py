import os
from azure.storage.blob import BlobServiceClient
from io import BytesIO


def upload_pdf(pdf_buffer: BytesIO, file_name: str) -> str:
    connection_string = os.environ['AZURE_STORAGE_CONNECTION_STRING']

    blob_service = BlobServiceClient.from_connection_string(connection_string)

    container = blob_service.get_container_client('invoices')

    if not container.exists():
        container.create_container()

    blob_client = container.get_blob_client(file_name)

    blob_client.upload_blob(pdf_buffer, overwrite=True)

    return blob_client.url