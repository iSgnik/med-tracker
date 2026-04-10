import json
import os
import argparse

def carregar_dados(arquivo="medicamentos.json"):
    """Carrega a lista de medicamentos do arquivo JSON."""
    if not os.path.exists(arquivo):
        return []
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)

def salvar_dados(dados, arquivo="medicamentos.json"):
    """Salva a lista de medicamentos no arquivo JSON."""
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)

def adicionar_medicamento(nome, horario, arquivo="medicamentos.json"):
    """Adiciona um novo medicamento após validar as entradas."""
    if not nome or not nome.strip():
        raise ValueError("O nome do medicamento não pode ser vazio.")
    if not horario or not horario.strip():
        raise ValueError("O horário não pode ser vazio.")
    
    dados = carregar_dados(arquivo)
    dados.append({"nome": nome.strip(), "horario": horario.strip()})
    salvar_dados(dados, arquivo)
    return True

def listar_medicamentos(arquivo="medicamentos.json"):
    """Retorna todos os medicamentos cadastrados."""
    return carregar_dados(arquivo)

def main():
    parser = argparse.ArgumentParser(description="MedTracker - Controle de Medicamentos")
    subparsers = parser.add_subparsers(dest="comando", help="Comandos disponíveis")

    # Comando: add
    parser_add = subparsers.add_parser("add", help="Adicionar um medicamento")
    parser_add.add_argument("--nome", required=True, help="Nome do medicamento")
    parser_add.add_argument("--horario", required=True, help="Horário (ex: 08:00)")

    # Comando: list
    subparsers.add_parser("list", help="Listar todos os medicamentos")

    args = parser.parse_args()

    try:
        if args.comando == "add":
            adicionar_medicamento(args.nome, args.horario)
            print(f"Sucesso! Medicamento '{args.nome}' adicionado para as {args.horario}.")
        elif args.comando == "list":
            meds = listar_medicamentos()
            if not meds:
                print("Nenhum medicamento cadastrado ainda.")
            else:
                print("\n--- Lista de Medicamentos ---")
                for m in meds:
                    print(f"⏰ {m['horario']} - 💊 {m['nome']}")
                print("-----------------------------\n")
        else:
            parser.print_help()
    except ValueError as e:
        print(f"Erro de validação: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
