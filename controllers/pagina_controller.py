from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from security.permissoes import exigir_permissao
from services.template_context_service import TemplateContextService


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/")
def login(request: Request):
  return templates.TemplateResponse(
    request=request, 
    name="login.html",
    context=TemplateContextService.criar(request))


@router.get("/pages/main")
def main(request: Request, sessao=Depends(exigir_permissao("ROTA_MAIN"))):
  return templates.TemplateResponse(
    request=request,
    name="main.html",
    context=TemplateContextService.criar(request))


@router.get("/pages/usuarios")
def usuarios(request: Request, sessao=Depends(exigir_permissao("ROTA_USUARIOS"))):
  return templates.TemplateResponse(
    request=request,
    name="usuarios.html",
    context=TemplateContextService.criar(request))


@router.get("/pages/acesso-negado")
def acesso_negado(request: Request):
  return templates.TemplateResponse(
    request=request,
    name="acesso-negado.html",
    context=TemplateContextService.criar(request))
