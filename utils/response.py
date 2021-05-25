from django.http import JsonResponse


class SuccessJsonResponse(JsonResponse):
    def __init__(self, data: dict = dict(), status=200, *args, **kwargs) -> None:
        data['status'] = 'success'
        super().__init__(data, status=status, *args, **kwargs)

# for bad request error code 400


class BadJsonResponse(JsonResponse):
    def __init__(self, data: dict = dict(), status=400, *args, **kwargs) -> None:
        data['status'] = 'error'
        super().__init__(data, status=status, *args, **kwargs)
