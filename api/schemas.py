from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class CategoriaCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=100)


class Categoria(CategoriaCreate):
    id: int


class ProdutoCreate(BaseModel):
    nome: str = Field(min_length=1, max_length=150)
    categoria_id: int
    preco: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    estoque: int = Field(ge=0)


class Produto(ProdutoCreate):
    id: int

class ItemVendaCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0)


class VendaCreate(BaseModel):
    itens: list[ItemVendaCreate] = Field(min_length=1)


class ItemVenda(BaseModel):
    produto_id: int
    quantidade: int
    preco_unitario: Decimal


class Venda(BaseModel):
    id: int
    data_hora: datetime
    total: Decimal
    itens: list[ItemVenda]