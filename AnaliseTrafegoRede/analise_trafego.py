import csv
import re
from collections import defaultdict

def analisar_trafego(arquivo_log='trafego.txt', arquivo_saida='relatorio.csv'):
    """
    Lê um arquivo de log do tcpdump, analisa os dados e gera um relatório CSV.

    A função extrai o IP de origem e a porta de destino de cada linha,
    conta o total de eventos por IP e detecta possíveis varreduras de porta.

    Args:
        arquivo_log (str): O caminho para o arquivo de log gerado pelo tcpdump.
        arquivo_saida (str): O caminho para o arquivo CSV de relatório a ser gerado.
    """
    # Usamos defaultdict para facilitar a inicialização de novos IPs.
    # A estrutura será: { 'ip_origem': {'count': 0, 'ports': set()} }
    ips_origem = defaultdict(lambda: {'count': 0, 'ports': set()})

    # Expressão regular para extrair o IP de origem e a porta de destino
    # Exemplo de linha: 0.000000 10.0.2.15.5353 > 224.0.0.251.5353: ...
    # O padrão busca pelo IP.PORTA de origem e depois pelo IP.PORTA de destino
    padrao = re.compile(r'\s+([\d\.]+)\.(\d+)\s+>\s+[\d\.]+\.(\d+):')

    print(f"Lendo o arquivo '{arquivo_log}'...")
    try:
        with open(arquivo_log, 'r') as f:
            for linha in f:
                # O formato esperado é: <timestamp> <ip_origem.porta> > <ip_destino.porta>: ...
                partes = linha.split()
                if len(partes) < 4 or partes[2] != '>':
                    continue

                try:
                    # Extrai o IP e a porta de origem
                    ip_origem_full = partes[1]
                    # rsplit('.', 1) divide a string no último ponto, separando IP da porta
                    ip_origem = ip_origem_full.rsplit('.', 1)[0]

                    # Extrai a porta de destino
                    porta_destino_full = partes[3]
                    # Remove o ':' do final e pega a porta
                    porta_destino = porta_destino_full.rstrip(':').rsplit('.', 1)[-1]
                    
                    if porta_destino.isdigit():
                        ips_origem[ip_origem]['count'] += 1
                        ips_origem[ip_origem]['ports'].add(int(porta_destino))

                except (IndexError, ValueError) as e:
                    # Ignora linhas que não correspondem ao formato esperado
                    # print(f"Linha ignorada por erro de formatação: {linha.strip()} - Erro: {e}")
                    pass

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_log}' não foi encontrado.")
        print("Certifique-se de executar o comando tcpdump primeiro.")
        return

    print(f"Análise concluída. Gerando o relatório '{arquivo_saida}'...")
    # Escreve os resultados no arquivo CSV
    with open(arquivo_saida, 'w', newline='') as f_csv:
        writer = csv.writer(f_csv)
        # Escreve o cabeçalho
        writer.writerow(['IP', 'Total_Eventos', 'Detectado_PortScan'])

        # Itera sobre os IPs encontrados para escrever os dados
        for ip, dados in ips_origem.items():
            # Define a condição para detecção de Port Scan
            port_scan_detectado = "Sim" if len(dados['ports']) > 10 else "Não"
            
            writer.writerow([ip, dados['count'], port_scan_detectado])

    print("Relatório gerado com sucesso!")


if __name__ == "__main__":
    analisar_trafego()

