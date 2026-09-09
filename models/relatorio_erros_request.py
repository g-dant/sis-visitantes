from pydantic import BaseModel
from typing import Any


class RelatorioErrosRequest(BaseModel):
    linhas: list[dict[str, Any]]
