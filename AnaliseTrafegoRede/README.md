# 📡 Ferramenta de Análise de Tráfego de Rede

Este projeto consiste em um script Python que analisa um arquivo de captura de tráfego de rede gerado pelo **tcpdump** para contar eventos por IP e detectar atividades suspeitas, como varredura de portas (**port scan**).

---

## 🚀 Como Executar

O processo é dividido em duas etapas principais, ambas executadas no terminal.

---

### 1️⃣ Captura de Tráfego com tcpdump

Primeiro, identifique a interface de rede ativa no seu sistema. Utilize o comando:

```bash
ip addr
Procure pela sua interface principal (ex: eth0, enp0s3, wlan0).

Em seguida, execute o tcpdump como superusuário (sudo) para capturar 60 segundos de tráfego de pacotes IP.
Substitua <interface> pelo nome da sua interface:

bash
Copiar código
sudo timeout 60s tcpdump -i <interface> -nn -ttt ip > trafego.txt
Esse comando criará o arquivo trafego.txt, que servirá de entrada para o script de análise.

2️⃣ Análise com o Script Python
Com o arquivo trafego.txt gerado, execute o script de análise diretamente no terminal:

bash
Copiar código
python3 analise_trafego.py
O script irá:

Ler o arquivo trafego.txt

Processar os dados

Gerar automaticamente o relatório relatorio.csv no mesmo diretório

Mensagens de progresso serão exibidas no terminal.

📊 Interpretação do relatorio.csv
O arquivo de saída relatorio.csv contém três colunas:

Coluna	Descrição
IP	O endereço IP de origem do tráfego.
Total_Eventos	Número total de pacotes (linhas no log) originados daquele IP.
Detectado_PortScan	"Sim" se o IP tentou acessar mais de 10 portas distintas em 60s, senão "Não".

⚠️ Limitações e Possíveis Melhorias
Tráfego Baixo: Em redes com pouco tráfego, a captura de 60 segundos pode não ser suficiente para detectar atividades anômalas.

Falsos Positivos: Um "Sim" na coluna Detectado_PortScan não é confirmação absoluta de ataque. Navegadores modernos podem abrir múltiplas conexões simultaneamente.

Falsos Negativos: Um atacante pode usar uma varredura lenta (slow scan), distribuída em mais de 60 segundos, dificultando a detecção.

Limite Fixo: O critério de "mais de 10 portas" é arbitrário. Em ambientes de produção, o valor deve ser ajustado com base no perfil de tráfego normal da rede (baseline).

markdown
Copiar código

Quer que eu já adicione uma seção **📦 Instalação** com dependências (ex.: Python 3, tcpdump, etc.) para deixar o README mais completo?
