from dotenv import load_dotenv
load_dotenv()

from config.app_config import NOME_SISTEMA

from controllers import ROUTERS
from controllers.pagina_controller import templates

from database.initializer import DatabaseInitializer

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from security.permissoes import exibir_item_menu, possui_permissao


app = FastAPI(title=NOME_SISTEMA)

DatabaseInitializer.inicializar()


@app.exception_handler(HTTPException)
async def tratar_http_exception(request: Request, exc: HTTPException):

  if request.url.path.startswith("/pages/"):
  
    if exc.status_code == 401:
      return RedirectResponse(
        url="/",
        status_code=303)
  
    if exc.status_code == 403:
      return RedirectResponse(
        url="/pages/acesso-negado",
        status_code=303)

  return JSONResponse(
    status_code=exc.status_code,
    content={ "detail": exc.detail })

templates.env.globals["exibir_item_menu"] = exibir_item_menu
templates.env.globals["possui_permissao"] = possui_permissao

app.mount("/static", StaticFiles(directory="static"), name="static")


for router in ROUTERS:
  app.include_router(router)
