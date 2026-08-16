import azure.functions as func
import datetime
import json
import logging

from models.invoice import Invoice
from pydantic import ValidationError

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.function_name('health')
@app.route(route='health', methods=['GET'])
def health(req: func.HttpRequest) -> func.HttpResponse:
    res = {
        'status': 'ok',
        'service': 'sig-app',
        'description': 'Health check for Serverless Invoice Generator API',
        'version': '0.1'
    }
    return func.HttpResponse(
        json.dumps(res),
        mimetype="application/json",
        status_code=200
    )

@app.function_name('invoices')
@app.route(route='invoices', methods=['POST'])
def invoices(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        invoice = Invoice.model_validate(req_body)

    except ValidationError as e:
        errors = []
        for err in e.errors():
            location = ' -> '.join(str(loc) for loc in err['loc'])
            errors.append(location)


        return func.HttpResponse(
            json.dumps({'message': 'This field is required.','errors': errors}),
            status_code=422,
            mimetype='application/json',
        )

    except ValueError:
        return func.HttpResponse(
            'Invalid JSON',
            status_code=422
        )

    output = {
        'invoice_id': invoice.invoice_id,
        'invoice_date': invoice.invoice_date,
        'invoice_url': ''
    }

    return func.HttpResponse(
        json.dumps(output),
        mimetype="application/json",
        status_code=201
    )
