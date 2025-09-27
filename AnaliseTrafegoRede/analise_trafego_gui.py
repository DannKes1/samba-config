
import csv
import re
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

# Importar as funções de análise do arquivo analise_trafego.py
# Para fins de integração, vamos copiar as funções diretamente aqui para evitar problemas de importação em um ambiente de execução simples.
# Em um projeto maior, seria preferível manter em arquivos separados e usar 'from analise_trafego import parse_line, analyze_traffic, generate_csv_report'

def parse_line(line):
    """
    Parses a single line from the tcpdump output file.
    Expected format: '0.000000 10.0.0.5.12345 > 192.168.1.2.80: S ...'
    Returns (timestamp, source_ip, source_port, dest_ip, dest_port) or None if parsing fails.
    """
    match = re.match(r'^(\d+\.\d+)\s+([0-9.]+)\.(\d+)\s+>\s+([0-9.]+)\.(\d+):.*$', line)
    if match:
        timestamp = float(match.group(1))
        source_ip = match.group(2)
        source_port = int(match.group(3))
        dest_ip = match.group(4)
        dest_port = int(match.group(5))
        return timestamp, source_ip, source_port, dest_ip, dest_port
    return None

def analyze_traffic(file_path, time_window=60, port_threshold=10):
    """
    Analyzes tcpdump traffic log to detect port scans.

    Args:
        file_path (str): Path to the tcpdump log file (trafego.txt).
        time_window (int): Time window in seconds to consider for port scan detection.
        port_threshold (int): Number of distinct ports to consider a port scan.

    Returns:
        list: A list of dictionaries, each representing an IP with its analysis.
    """
    ip_activity = defaultdict(lambda: {
        'total_events': 0,
        'ports_accessed': defaultdict(list), # {port: [timestamp1, timestamp2, ...]}
        'timestamps': [] # All timestamps for this IP
    })

    try:
        with open(file_path, 'r') as f:
            for line in f:
                parsed_data = parse_line(line)
                if parsed_data:
                    timestamp, source_ip, _, _, dest_port = parsed_data
                    ip_activity[source_ip]['total_events'] += 1
                    ip_activity[source_ip]['ports_accessed'][dest_port].append(timestamp)
                    ip_activity[source_ip]['timestamps'].append(timestamp)
    except FileNotFoundError:
        messagebox.showerror("Erro", f"O arquivo '{file_path}' não foi encontrado.")
        return []
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao ler ou processar o arquivo: {e}")
        return []

    results = []
    for ip, data in ip_activity.items():
        port_scan_detected = "Não"
        
        # Sort timestamps to easily check within a sliding window
        data['timestamps'].sort()

        # Check for port scan within the time window
        for i in range(len(data['timestamps'])):
            start_time = data['timestamps'][i]
            end_time = start_time + time_window
            
            distinct_ports_in_window = set()
            for port, timestamps_list in data['ports_accessed'].items():
                for ts in timestamps_list:
                    if start_time <= ts < end_time:
                        distinct_ports_in_window.add(port)
            
            if len(distinct_ports_in_window) > port_threshold:
                port_scan_detected = "Sim"
                break # Found a scan, no need to check further for this IP

        results.append({
            'IP': ip,
            'Total_Eventos': data['total_events'],
            'Detectado_PortScan': port_scan_detected
        })
    
    return results

def generate_csv_report(results, output_file='relatorio.csv'):
    """
    Generates a CSV report from the analysis results.

    Args:
        results (list): List of dictionaries with analysis results.
        output_file (str): Name of the output CSV file.
    """
    if not results:
        messagebox.showinfo("Aviso", "Nenhum dado para gerar o relatório CSV.")
        return

    fieldnames = ['IP', 'Total_Eventos', 'Detectado_PortScan']
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(results)
        # print(f"Relatório '{output_file}' gerado com sucesso.") # Não imprimir no console em GUI
    except IOError as e:
        messagebox.showerror("Erro", f"Erro ao escrever o arquivo CSV '{output_file}': {e}")


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Analisador de Tráfego de Rede")
        self.root.geometry("600x450")
        self.caminho_arquivo_log = ""

        # --- Frame principal ---
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Botões e Label ---
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=5)

        self.btn_selecionar = ttk.Button(control_frame, text="Selecionar Arquivo de Log", command=self.selecionar_arquivo)
        self.btn_selecionar.pack(side=tk.LEFT, padx=(0, 10))

        self.lbl_arquivo = ttk.Label(control_frame, text="Nenhum arquivo selecionado")
        self.lbl_arquivo.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.btn_analisar = ttk.Button(main_frame, text="Analisar Tráfego e Gerar Relatório", command=self.executar_analise)
        self.btn_analisar.pack(fill=tk.X, pady=10)

        # --- Tabela de Resultados (Treeview) ---
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=('IP', 'Eventos', 'PortScan'), show='headings')
        self.tree.heading('IP', text='IP de Origem')
        self.tree.heading('Eventos', text='Total de Eventos')
        self.tree.heading('PortScan', text='Port Scan Detectado')
        
        self.tree.column('IP', width=150)
        self.tree.column('Eventos', width=100, anchor=tk.CENTER)
        self.tree.column('PortScan', width=150, anchor=tk.CENTER)

        # Scrollbar para a tabela
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def selecionar_arquivo(self):
        """Abre uma janela para o usuário selecionar o arquivo de log."""
        self.caminho_arquivo_log = filedialog.askopenfilename(
            title="Selecione o arquivo trafego.txt",
            filetypes=(("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*"))
        )
        if self.caminho_arquivo_log:
            # Mostra apenas o nome do arquivo para não ocupar muito espaço
            nome_arquivo = self.caminho_arquivo_log.split('/')[-1]
            self.lbl_arquivo.config(text=nome_arquivo)
        else:
            self.lbl_arquivo.config(text="Nenhum arquivo selecionado")

    def executar_analise(self):
        """Executa a análise do log, exibe os resultados na tabela e salva o CSV."""
        if not self.caminho_arquivo_log:
            messagebox.showwarning("Aviso", "Por favor, selecione um arquivo de log primeiro.")
            return

        # Limpa resultados anteriores da tabela
        for i in self.tree.get_children():
            self.tree.delete(i)

        # Analisa os dados usando a função aprimorada
        resultados_dict = analyze_traffic(self.caminho_arquivo_log)
        
        if not resultados_dict:
            return

        # Popula a tabela com os novos resultados
        for item in resultados_dict:
            self.tree.insert('', tk.END, values=(item['IP'], item['Total_Eventos'], item['Detectado_PortScan']))

        # Salva o relatório em CSV
        generate_csv_report(resultados_dict)

        messagebox.showinfo("Sucesso", "Análise concluída e relatório 'relatorio.csv' foi salvo com sucesso!")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()


