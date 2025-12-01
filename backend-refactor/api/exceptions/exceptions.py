from fastapi import HTTPException


class AssetNotFoundException(HTTPException):
    def __init__(self, asset_id):
        super().__init__(status_code=404, detail=f"Asset with ID {asset_id} not found")


class AssetAlreadyExistsException(HTTPException):
    def __init__(self, asset_id: str):
        super().__init__(
            status_code=409, detail=f"Asset with asset_id '{asset_id}' already exists"
        )


class SignalNotFoundException(HTTPException):
    def __init__(self, signal_id):
        super().__init__(
            status_code=404, detail=f"Signal with ID {signal_id} not found"
        )


class MeasurementNotFoundException(HTTPException):
    def __init__(self, measurement_id):
        super().__init__(
            status_code=404, detail=f"Measurement with ID {measurement_id} not found"
        )


class InvalidFieldException(HTTPException):
    def __init__(self, field: str, value):
        super().__init__(
            status_code=422, detail=f"Invalid value for field '{field}': {value}"
        )
