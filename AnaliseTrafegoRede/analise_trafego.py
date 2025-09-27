import csv
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
    ips_origem = defaultdict(lambda: {'count': 0, 'ports': set()})

    print(f"Lendo o arquivo '{arquivo_log}'...")
    try:
        with open(arquivo_log, 'r') as f:
            for linha in f:
                partes = linha.strip().split()
                
                # CORREÇÃO: A verificação agora checa se há pelo menos 5 partes,
                # para acomodar a palavra 'IP' extra no output.
                # Ex: ['00:00:00.000000', 'IP', '18.97.36.78.443', '>', '10.0.2.15.49178:']
                if len(partes) < 5:
                    continue

                try:
                    # CORREÇÃO: O IP de origem está na posição 2 (partes[2])
                    ip_origem_full = partes[2]
                    # CORREÇÃO: A porta de destino está na posição 4 (partes[4])
                    porta_destino_full = partes[4]

                    # Extrai o IP removendo a porta de origem
                    ip_origem = ip_origem_full.rsplit('.', 1)[0]
                    
                    # Extrai a porta de destino removendo o IP e os dois pontos
                    porta_destino_str = porta_destino_full.rstrip(':').rsplit('.', 1)[-1]
                    
                    if porta_destino_str.isdigit():
                        porta_destino = int(porta_destino_str)
                        ips_origem[ip_origem]['count'] += 1
                        ips_origem[ip_origem]['ports'].add(porta_destino)

                except (IndexError, ValueError):
                    # Ignora linhas que não correspondem ao formato esperado
                    pass

    except FileNotFoundError:
        print(f"Erro: O arquivo '{arquivo_log}' não foi encontrado.")
        print("Certifique-se de executar o comando tcpdump primeiro.")
        return

    print(f"Análise concluída. Gerando o relatório '{arquivo_saida}'...")
    with open(arquivo_saida, 'w', newline='') as f_csv:
        writer = csv.writer(f_csv)
        writer.writerow(['IP', 'Total_Eventos', 'Detectado_PortScan'])

        for ip, dados in ips_origem.items():
            # A regra de detecção de port scan permanece a mesma (mais de 10 portas distintas)
            port_scan_detectado = "Sim" if len(dados['ports']) > 10 else "Não"
            writer.writerow([ip, dados['count'], port_scan_detectado])

    print("Relatório gerado com sucesso!")


if __name__ == "__main__":
    analisar_trafego()
