from uuid import uuid4
from datetime import datetime
from datetime import timedelta

from repositories.sessao_repository import (SessaoRepository)

id_sessao = (
  SessaoRepository.criar(
    2,
    str(uuid4()),
    datetime.now(),
    datetime.now() + timedelta(hours=8)
  )
)

print(f"Sessão criada: {id_sessao}")
