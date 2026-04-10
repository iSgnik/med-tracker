import pytest
import os
import sys

# Adiciona a pasta src ao path para os testes conseguirem importar o med_tracker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from med_tracker import adicionar_medicamento, listar_medicamentos  # noqa: E402

ARQUIVO_TESTE = "test_medicamentos.json"


@pytest.fixture(autouse=True)
def preparar_ambiente():
    """Garante que o arquivo de teste seja deletado antes e depois de cada teste."""
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)
    yield
    if os.path.exists(ARQUIVO_TESTE):
        os.remove(ARQUIVO_TESTE)


def test_adicionar_medicamento_sucesso():
    """Teste 1: Caminho feliz (Cadastro correto)"""
    sucesso = adicionar_medicamento("Losartana", "08:00", ARQUIVO_TESTE)
    dados = listar_medicamentos(ARQUIVO_TESTE)

    assert sucesso is True
    assert len(dados) == 1
    assert dados[0]["nome"] == "Losartana"
    assert dados[0]["horario"] == "08:00"


def test_adicionar_medicamento_nome_invalido():
    """Teste 2: Entrada inválida (Nome vazio)"""
    with pytest.raises(ValueError, match="O nome do medicamento não pode ser vazio."):
        adicionar_medicamento("", "12:00", ARQUIVO_TESTE)


def test_listar_medicamentos_banco_vazio():
    """Teste 3: Caso limite (Ler arquivo quando não há medicamentos)"""
    dados = listar_medicamentos(ARQUIVO_TESTE)
    assert isinstance(dados, list)
    assert len(dados) == 0
