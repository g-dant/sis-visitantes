import os
import time

import jwt


class TokenQRCodeService:

  @staticmethod
  def gerar_token(id_autorizacao: int):

    payload = {
      "ver": 1,
      "iss": "SIS-Visitantes",
      "iat": int(time.time()),
      "id_autorizacao": id_autorizacao
    }

    return jwt.encode(
      payload,
      os.environ["QRCODE_SECRET"],
      algorithm="HS256"
    )

  @staticmethod
  def validar_token(token: str):

    return jwt.decode(
      token,
      os.environ["QRCODE_SECRET"],
      algorithms=["HS256"]
    )

  @staticmethod
  def obter_id_autorizacao(token: str):
  
    payload = TokenQRCodeService.validar_token(token)
  
    if payload["ver"] != 1:
      raise Exception("Versão de QR Code inválida.")
  
    return payload["id_autorizacao"]
