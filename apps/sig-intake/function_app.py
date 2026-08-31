import azure.functions as func
import datetime
import json
import logging

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.function_name('health')
@app.route(route='/health', methods=['GET'])
def health(req: func.HttpRequest) -> func.HttpResponse:
    res = {
        'status': 'ok',
        'service': 'sig-intake',
        'description': 'Health check',
        'version': '0.1'
    }
    return func.HttpResponse(json.dumps(res), mimetype='application/json', status_code=200)
