from sqlalchemy import create_engine


def createEngine(dbAddress: str):
    return create_engine(dbAddress, echo=True)
