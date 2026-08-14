from controllers.auth_controller import router as auth_router
from controllers.usuario_controller import router as usuario_router
from controllers.pagina_controller import router as pagina_router
from controllers.tipo_usuario_controller import router as tipo_usuario_router
from controllers.credencial_controller import router as credencial_router
from controllers.local_controller import router as local_router
from controllers.setor_controller import router as setor_router
from controllers.status_autorizacao_controller import router as status_autorizacao_router
from controllers.empresa_controller import router as empresa_router
from controllers.veiculo_controller import router as veiculo_router
from controllers.visitante_controller import router as visitante_router
from controllers.visitante_veiculo_controller import router as visitante_veiculo_router
from controllers.autorizacao_controller import router as autorizacao_router
from controllers.historico_autorizacao_controller import router as historico_autorizacao_router
from controllers.parametro_sistema_controller import router as parametro_sistema_router
from controllers.emissao_autorizacao_controller import router as emissao_autorizacao_router
from controllers.painel_autorizacao_controller import router as painel_autorizacao_router
from controllers.qrcode_controller import router as qrcode_router


ROUTERS = [
  pagina_router,

  auth_router,
  usuario_router,

  tipo_usuario_router,
  credencial_router,
  local_router,
  setor_router,
  status_autorizacao_router,

  empresa_router,
  veiculo_router,
  visitante_router,
  visitante_veiculo_router,

  autorizacao_router,
  historico_autorizacao_router,

  parametro_sistema_router,
  emissao_autorizacao_router,

  painel_autorizacao_router,
  qrcode_router,
]
