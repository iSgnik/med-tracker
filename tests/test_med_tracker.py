import pytest
import os
import sys
from unittest.mock import patch

# Adiciona a pasta src ao path para os testes conseguirem importar o med_tracker
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from med_tracker import adicionar_medicamento, listar_medicamentos, buscar_info_medicamento  # noqa: E402

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


@patch('med_tracker.requests.get')
def test_buscar_info_medicamento_sucesso(mock_get):
    """Teste 4: Integração com API (Simulando uma resposta de sucesso da Wikipedia)."""
    # Configura o 'mock' (dublê) para fingir que a API retornou código 200 e um JSON com o texto
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"extract": "A Dipirona é um analgésico e antitérmico."}
    
    resultado = buscar_info_medicamento("Dipirona")
    
    # Valida se o sistema repassou a string corretamente e se chamou a URL certa
    assert resultado == "A Dipirona é um analgésico e antitérmico."
    mock_get.assert_called_once_with("https://pt.wikipedia.org/api/rest_v1/page/summary/Dipirona", timeout=5)
