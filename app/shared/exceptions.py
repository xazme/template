from fastapi.exceptions import HTTPException


class ExceptionRaiser:

    @staticmethod
    def raise_exception(status_code: int):
        raise HTTPException(status_code=status_code)
