Ferramenta de Análise de Tráfego de Rede
Este projeto consiste em um script Python que analisa um arquivo de captura de tráfego de rede gerado pelo tcpdump para contar eventos por IP e detectar atividades suspeitas, como varredura de portas (port scan).

Como Executar
O processo é dividido em duas etapas principais, ambas executadas no terminal.

1. Captura de Tráfego com tcpdump
Primeiro, você precisa identificar a interface de rede ativa no seu sistema. Utilize o comando:

ip addr

Procure pela sua interface principal (ex: eth0, enp0s3, wlan0).

Em seguida, execute o tcpdump como superusuário (sudo) para capturar 60 segundos de tráfego de pacotes IP. Substitua <interface> pelo nome da sua interface.

sudo timeout 60s tcpdump -i <interface> -nn -ttt ip > trafego.txt

Este comando criará o arquivo trafego.txt, que servirá de entrada para o script de análise.

2. Análise com o Script Python
Com o arquivo trafego.txt gerado, execute o script de análise diretamente no terminal:

python3 analise_trafego.py

O script irá ler o arquivo trafego.txt, processar os dados e gerar automaticamente o relatório relatorio.csv no mesmo diretório. Mensagens de progresso serão exibidas no terminal.

Interpretação do relatorio.csv
O arquivo de saída relatorio.csv contém três colunas:

Coluna

Descrição

IP

O endereço IP de origem do tráfego.

Total_Eventos

O número total de pacotes (linhas no log) originados a partir daquele endereço IP durante a captura.

Detectado_PortScan

Indica se foi detectada uma possível varredura de portas. O valor será "Sim" se o IP de origem tentou se conectar a mais de 10 portas de destino distintas no período de 60 segundos. Caso contrário, será "Não".

Limitações e Possíveis Melhorias
Tráfego Baixo: Em uma rede com pouco tráfego, a captura de 60 segundos pode não ser suficiente para detectar atividades anômalas ou gerar um relatório significativo.

Falsos Positivos: Um "Sim" na coluna Detectado_PortScan não é uma confirmação absoluta de um ataque. Um navegador web moderno, por exemplo, pode se conectar a múltiplos serviços e portas distintas em um curto período, o que poderia ser interpretado incorretamente como um port scan.

Falsos Negativos: Um atacante pode realizar uma varredura "lenta" (slow scan), distribuindo as tentativas de conexão ao longo de um período maior que 60 segundos para evitar detecção.

Limite Fixo: O critério de "mais de 10 portas" é um limiar arbitrário. Para um ambiente de produção, este valor deveria ser ajustado com base no perfil de tráfego normal da rede (baseline).
