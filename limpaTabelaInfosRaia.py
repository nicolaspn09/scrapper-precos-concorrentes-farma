import requests

# Função para informar a tabela
def limpa_tabela():
    # Grava a informação de situação no Google sheet do DP
    action = f"?action=clear"
    
    url = f"https://script.google.com/macros/s/AKfycbyF1nXO_gm2hJKB8XPjKsOAZBCnzkyyvBRNw_sKfzHpOVoF69gwgRgqJMyfOpnqHSNg/exec{action}"

    # Fazendo a requisição para a API
    requests.get(url)


limpa_tabela()