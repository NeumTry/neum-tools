from .Pipeline import Pipeline
from .Pipeline import Pipeline
from fastapi.responses import JSONResponse
from typing import Union

class PipelineModel(JSONResponse):
    def __init__(
        self,
        content: Union[Pipeline,Pipeline],
        status_code: int = 200,
    ) -> None:
        super().__init__(content, status_code, headers=None, media_type="application/json", background=None)

class PipelinesModel(JSONResponse):
    def __init__(
        self,
        content: dict,
        status_code: int = 200,
    ) -> None:
        super().__init__(content, status_code, headers=None, media_type="application/json", background=None)

class PipelineSearchResultsModel(JSONResponse):
    def __init__(
        self,
        content: dict,
        status_code: int = 200,
    ) -> None:
        super().__init__(content, status_code, headers=None, media_type="application/json", background=None)