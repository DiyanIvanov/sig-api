
class CSVValidationError(Exception):
    def __init__(self, errors: list) -> None:
        self.errors = errors
        super().__init__('Invalid CSV file')


class CSVParseError(Exception):
    pass