from datetime import datetime, timedelta

from fastapi import APIRouter, HTTPException, Request, Response

from models.login_request import LoginRequest

from repositories.sessao_repository import SessaoRepository

from services.auth_service import AuthService
from services.sessao_service import SessaoService

from uuid import uuid4


router = APIRouter()


@router.post("/pages/login")
def login(request: LoginRequest, response: Response):

  usuario = AuthService.autenticar(request.email, request.senha)
  if usuario is None:
    raise HTTPException(status_code=401, detail="Usuário ou senha inválidos")

  token = str(uuid4())
  agora = datetime.now()
  expira = agora + timedelta(hours=8)

  SessaoRepository.criar(usuario["id"], token, agora, expira)
  sessao = SessaoRepository.buscar_sessao_ativa(token)
 
  response.set_cookie(
    key="token",
    value=token,
    httponly=True,
    samesite="lax",
    secure=False)

  return {
    "token": token,
    "usuario": SessaoService.obter_contexto(sessao) }


@router.post("/logout")
def logout(request: Request, response: Response):

  token = request.cookies.get("token")

  if token is not None:
    SessaoRepository.encerrar(token)

  response.delete_cookie("token")

  return { "mensagem": "Sessão encerrada." }
