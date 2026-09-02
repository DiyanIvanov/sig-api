# SIG Platform

A serverless invoice processing platform built with **Python and Azure Functions**.

SIG Platform ingests invoice data as either a CSV upload or direct JSON, validates and transforms it, generates PDF invoices, and stores them in Azure Blob Storage. An Azure Logic App orchestrates the CSV processing flow between `sig-intake` and `sig-api`.

> **Note:** This is a portfolio project built to explore serverless architecture, workflow orchestration, CI/CD, and Azure cloud services.

## Overview

The platform consists of an orchestrator and two independently deployed Azure Function Apps:

| Component | Responsibility |
|---|---|
| **Logic App (orchestrator)** | Coordinates the workflow — sends the incoming CSV to `sig-intake`, then forwards the resulting invoice(s) to `sig-api`. |
| **`sig-intake`** | Accepts CSV uploads, validates and transforms the data into invoice records. |
| **`sig-api`** | Validates invoice data, generates PDF invoices using ReportLab, and stores them in Azure Blob Storage. Accepts invoice JSON directly. |

Each Function App has its own dependencies, its own deployment pipeline, and can be developed and released on its own schedule. The Logic App owns the orchestration logic and sequencing between them.

## Architecture

```
CSV Upload
    │
    ▼
Azure Logic App (orchestrator)
    │
    │ 1. Send CSV
    ▼
SIG Intake
    │
    │ Parse & Validate
    ▼
Invoice JSON
    │
    │ 2. Forward result
    ▼
Azure Logic App (orchestrator)
    │
    ▼
SIG API
    │
    │ Generate PDF
    ▼
Azure Blob Storage
```

Invoice data can also be submitted directly to `sig-api` as JSON, bypassing the Logic App and `sig-intake` entirely.

## Tech Stack

- **Python** — core language for both Function Apps
- **Azure Functions** — serverless compute
- **Azure Logic Apps** — workflow orchestration between `sig-intake` and `sig-api`
- **Azure Blob Storage** — PDF invoice storage
- **Pydantic** — data validation and modeling
- **pandas** — CSV parsing and transformation
- **ReportLab** — PDF generation
- **Azurite** — local Azure Storage emulator
- **GitHub Actions** — CI/CD

## Project Structure

```
sig-platform/
├── sig-api/
├── sig-intake/
├── sig-orchestrator/        # Azure Logic App workflow definition
├── .github/
│   └── workflows/
└── README.md
```

Each Function App maintains its own `requirements.txt` and is deployed independently through GitHub Actions.

## Getting Started

### Prerequisites

- Python 3.14+
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- [Azurite](https://learn.microsoft.com/en-us/azure/storage/common/storage-use-azurite) (for local Blob Storage emulation)

### Local Development

Each Function App is run independently. From the app's directory:

```bash
cd sig-api
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
func start
```

The same process applies to `sig-intake`:

```bash
cd sig-intake
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
func start
```

> Make sure Azurite is running locally if either app depends on Blob Storage.

## Deployment

Each Function App is deployed independently via GitHub Actions, defined under `.github/workflows/`. Pushes to the relevant branch trigger the corresponding app's pipeline.

The Logic App workflow definition is deployed alongside them, and its HTTP actions must point at the deployed `sig-intake` and `sig-api` endpoints (update these per environment).

## License

This project is licensed under the MIT License. See the [`LICENSE`](./LICENSE) file for details.
