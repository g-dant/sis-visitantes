from datetime import datetime


class DataUtils:

  FORMATOS_ACEITOS = [
    "%Y-%m-%d",
    "%d/%m/%Y",
    "%d-%m-%Y",
    "%Y/%m/%d",
  ]

  @staticmethod
  def parse(data):

    if data is None:
      return None

    if not isinstance(data, str):
      return data

    data = data.strip()

    if data == "":
      return None

    for formato in DataUtils.FORMATOS_ACEITOS:

      try:
        return datetime.strptime(data, formato).date()

      except ValueError:
        pass

    return None

  @staticmethod
  def formatar(data):

    if data is None:
      return ""

    return data.strftime("%d/%m/%Y")
