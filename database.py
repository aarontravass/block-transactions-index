from sqlalchemy import create_engine
import psycopg2

def createEngine(dbAddress: str):
    return create_engine(dbAddress, echo=True)
