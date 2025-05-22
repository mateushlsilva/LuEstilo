from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from app.config import settings

class Database:
    def __init__(self):
        self.engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        

    def get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
            print("✅ Conexão com o banco bem-sucedida!")
        except Exception as e:
            print("❌ Erro ao conectar no banco de dados:")
            print(e)
            raise
        finally:
            db.close()
        
Base = declarative_base()