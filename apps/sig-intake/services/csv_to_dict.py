from typing import List
from exceptions import CSVValidationError, CSVParseError
import pandas as pd


REQUIRED_COLUMNS = {
    'customer',
    'invoice_id',
    'invoice_date',
    'name',
    'price',
    'quantity'
}

def validate_csv_schema(df: pd.DataFrame) -> List[str]:
    errors = []
    missing = REQUIRED_COLUMNS - set(df.columns)

    if missing:
        errors.append(f'Missing required columns: {", ".join(missing)}')
    if df.empty:
        errors.append('No data found')

    return errors


def csv_to_dict(csv_file):
    try:
        df = pd.read_csv(csv_file)
    except (pd.errors.ParserError, UnicodeDecodeError) as e:
        raise CSVParseError("Unable to parse CSV file") from e

    errors = validate_csv_schema(df)

    if errors:
        raise CSVValidationError(errors)

    res = {}
    for (customer, invoice_id, invoice_date), group in df.groupby(['customer', 'invoice_id', 'invoice_date']):
        tmp = {
            'customer': customer,
            'invoice_id': invoice_id,
            'invoice_date': invoice_date,
            'products': group[['name', 'price', 'quantity']].to_dict(orient='records')
        }

        res.update(tmp)

    return res


