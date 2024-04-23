from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from typing import Optional


class Base(DeclarativeBase):
    pass


class Block(Base):
    __tablename__ = "Block"
    blockNumber: Mapped[str] = mapped_column(String(256), primary_key=True)
    hash: Mapped[str]
    timestamp: Mapped[int]
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="block", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Block(blockNumber={self.blockNumber!r})"


class Transaction(Base):
    __tablename__ = "Transaction"
    txHash: Mapped[int] = mapped_column(String(256), primary_key=True)
    value: Mapped[Optional[str]]
    fromAddress: Mapped[Optional[str]]
    toAddress: Mapped[Optional[str]]
    blockNumber: Mapped[str] = mapped_column(ForeignKey("Block.blockNumber"))
    block: Mapped["Block"] = relationship(back_populates="transactions")

    def __repr__(self) -> str:
        return f"Transaction(txHash={self.txHash!r})"
