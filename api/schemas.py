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