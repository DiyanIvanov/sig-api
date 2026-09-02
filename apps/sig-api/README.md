# SIG API — Serverless Invoice Generator

A serverless Azure Functions API (Python) that generates PDF invoices and uploads them to Azure Blob Storage.

## Endpoints

### `GET /api/health`
Health check.

```json
{ "status": "ok", "service": "sig-app", "version": "0.1" }
```

### `POST /api/invoices`
Generates a PDF invoice, uploads it to Blob Storage, and returns a link to download it.

**Response `201`:**
```json
{
  "invoice_id": "INV-001",
  "invoice_date": "2026-08-16",
  "invoice_url": "https://.../invoices/INV-001.pdf?<sas-token>"
}
```

## Tech Stack

Python · Azure Functions · ReportLab · Pydantic · Azure Blob Storage

## Running Locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
func start
```

Requires Azurite running locally for blob storage, and a `local.settings.json` with `AZURE_STORAGE_CONNECTION_STRING` set.

## Deployment

Deployed to Azure Functions via GitHub Actions. Blob links use short-lived SAS tokens rather than public access.
