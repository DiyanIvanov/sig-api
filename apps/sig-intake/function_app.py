import azure.functions as func
import datetime
import json
import logging
from exceptions import CSVParseError, CSVValidationError
from models import Invoice
from services import csv_to_dict

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name('health')
@app.route(route='health/', methods=['GET'])
def health(req: func.HttpRequest) -> func.HttpResponse:
    res = {
        'status': 'ok',
        'service': 'sig-intake',
        'description': 'Health check',
        'version': '0.1'
    }
    return func.HttpResponse(json.dumps(res), mimetype='application/json', status_code=200)


@app.function_name('generate_invoices')
@app.route(route='generate_invoices/', methods=['POST'])
def generate_invoices(req: func.HttpRequest) -> func.HttpResponse:
    try:
        data = req.files['file']
    except KeyError:
        return func.HttpResponse(
            'No CSV file found',
            status_code=422,
            mimetype='application/json'
        )

    try:
        res = csv_to_dict(data)
    except (CSVValidationError, CSVParseError) as e:
        return func.HttpResponse(
            str(e),
            status_code=422,
            mimetype='application/json'
        )

    invoice = Invoice.model_validate(res)

    return func.HttpResponse(json.dumps(invoice.dict()), mimetype='application/json', status_code=200)
