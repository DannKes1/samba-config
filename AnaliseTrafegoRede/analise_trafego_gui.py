import csv
import re
from collections import defaultdict
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

def analisar_dados_log(caminho_arquivo):
    """
    Lê um arquivo de log do tcpdump e retorna os dados analisados.

    Args:
        caminho_arquivo (str): O caminho para o arquivo de log.

    Returns:
        list: Uma lista de listas contendo os dados do relatório.
              Retorna None se o arquivo não for encontrado.
    """
    ips_origem = defaultdict(lambda: {'count': 0, 'ports': set()})

    try:
        with open(caminho_arquivo, 'r') as f:
            for linha in f:
                partes = linha.split()
                if len(partes) < 4 or partes[2] != '>':
                    continue

                try:
                    ip_origem_full = partes[1]
                    ip_origem = ip_origem_full.rsplit('.', 1)[0]
                    porta_destino_full = partes[3]
                    porta_destino = porta_destino_full.rstrip(':').rsplit('.', 1)[-1]
                    
                    if porta_destino.isdigit():
                        ips_origem[ip_origem]['count'] += 1
                        ips_origem[ip_origem]['ports'].add(int(porta_destino))
                except (IndexError, ValueError):
                    pass
    except FileNotFoundError:
        messagebox.showerror("Erro", f"O arquivo '{caminho_arquivo}' não foi encontrado.")
        return None

    # Prepara os resultados para serem retornados
    resultados = []
    for ip, dados in sorted(ips_origem.items()):
        port_scan_detectado = "Sim" if len(dados['ports']) > 10 else "Não"
        resultados.append([ip, dados['count'], port_scan_detectado])
    
    return resultados

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

        # Analisa os dados
        resultados = analisar_dados_log(self.caminho_arquivo_log)
        
        if resultados is None:
            return

        # Popula a tabela com os novos resultados
        for item in resultados:
            self.tree.insert('', tk.END, values=item)

        # Salva o relatório em CSV
        self.salvar_csv(resultados)

        messagebox.showinfo("Sucesso", "Análise concluída e relatório 'relatorio.csv' foi salvo com sucesso!")

    def salvar_csv(self, dados, arquivo_saida='relatorio.csv'):
        """Salva os dados analisados em um arquivo CSV."""
        with open(arquivo_saida, 'w', newline='') as f_csv:
            writer = csv.writer(f_csv)
            writer.writerow(['IP', 'Total_Eventos', 'Detectado_PortScan'])
            writer.writerows(dados)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
