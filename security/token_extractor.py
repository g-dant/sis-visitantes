from fastapi import Request


from fastapi import Request


class TokenExtractor:

  @staticmethod
  def extrair(request: Request):

    token = request.cookies.get("token")

    if token is not None:
      return token

    authorization = request.headers.get("Authorization")

    if authorization is None:
      return None

    if not authorization.startswith("Bearer "):
      return None

    return authorization.replace("Bearer ", "")
