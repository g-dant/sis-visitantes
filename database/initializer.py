from pathlib import Path

from config.database import get_connection


from pathlib import Path

from config.database import get_connection


class DatabaseInitializer:

  @staticmethod
  def inicializar():

    conn = get_connection()

    try:

      with conn.cursor() as cursor:

        cursor.execute("""
          SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_type = 'BASE TABLE')""")

        banco_possui_tabelas = cursor.fetchone()["exists"]

        if banco_possui_tabelas:
          return

        schema_path = (
          Path(__file__).resolve().parent / "schema.sql")

        schema = schema_path.read_text(encoding="utf-8")

        cursor.execute(schema)

      conn.commit()

    except Exception:
      conn.rollback()
      raise

    finally:
      conn.close()
