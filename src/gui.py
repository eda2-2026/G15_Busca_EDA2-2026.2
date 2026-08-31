# ============================================================
# ARQUIVO: src/gui.py
#
# DESCRIÇÃO:
#   - Interface gráfica simples (Tkinter)
#
# COMO EXECUTAR:
#   python3 src/gui.py
#
# ABAS:
#   - Buscar  : busca por ID (indexada + sequencial) ou por
#               Título (hash + sequencial), mostrando o tempo
#               e o nº de comparações/operações de cada método.
#   - Inserir : formulário para adicionar um novo filme.
#   - Excluir : remove por ID ou por Título (se houver mais de
#               um filme com o mesmo título, permite escolher).
#
# OBSERVAÇÕES:
#   - Ao fechar a janela, pergunta se deseja salvar as alterações no CSV.
# ============================================================
import os
import sys
import time
import tkinter as tk
from tkinter import ttk, messagebox

sys.path.append(os.path.dirname(__file__))

from leitura_csv import carregar_csv, salvar_csv, normalizar_titulo
from busca_indexada import construir_indice, buscar_por_id_comparacoes, inserir_filme, excluir_filme
from busca_sequencial import buscar_por_nome_sequencial, buscar_por_id_sequencial_comparacoes, buscar_por_nome_sequencial_comparacoes
from busca_hash import criar_hash_titulos, buscar_por_hash_titulos_operacoes

CAMPOS_INSERIR = [
    ("Título", "Título da obra"),
    ("Ano", "Ano de exibição"),
    ("Gênero", "Gênero"),
    ("País produtor", "País(es) produtor(es) da obra"),
    ("Nacionalidade", "Nacionalidade da obra"),
    ("Distribuidora", "Empresa distribuidora"),
    ("Origem da distribuidora", "Origem da empresa distribuidora"),
]

class AppFilmes(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Busca de Filmes")
        self.geometry("880x560")
        self.minsize(760, 480)

        self.caminho_csv = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "filmes.csv",
        )
        self.filmes = carregar_csv(self.caminho_csv)

        if not self.filmes:
            messagebox.showerror(
                "Erro", f"Não foi possível carregar '{self.caminho_csv}'."
            )
            self.destroy()
            return

        self.blocos, self.indice = construir_indice(self.filmes)
        self.hash_titulos = criar_hash_titulos(self.filmes)
        self.alteracoes_pendentes = False

        # --- lista de títulos únicos, usada pelo autocomplete da busca ---
        self.titulos_unicos = []
        self._chaves_titulos_vistas = set()
        for filme in self.filmes:
            self._registrar_titulo_para_autocomplete(filme["Título da obra"])
        self.titulos_unicos.sort(key=normalizar_titulo)

        # --- estado do autocomplete (o widget em si é criado na aba) ---
        self.lista_sugestoes = None

        self.protocol("WM_DELETE_WINDOW", self._ao_fechar)

        self._montar_layout()

    # ==========================================================
    # LAYOUT GERAL
    # ==========================================================
    def _montar_layout(self):
        barra_status = ttk.Label(
            self,
            text=f"{len(self.filmes)} filmes carregados de '{os.path.basename(self.caminho_csv)}'",
            anchor="w",
            padding=(8, 4),
        )
        barra_status.pack(side="bottom", fill="x")
        self.barra_status = barra_status

        abas = ttk.Notebook(self)
        abas.pack(fill="both", expand=True, padx=8, pady=8)

        aba_buscar = ttk.Frame(abas)
        aba_inserir = ttk.Frame(abas)
        aba_excluir = ttk.Frame(abas)

        abas.add(aba_buscar, text="🔍 Buscar")
        abas.add(aba_inserir, text="➕ Inserir")
        abas.add(aba_excluir, text="🗑️ Excluir")

        self._montar_aba_buscar(aba_buscar)
        self._montar_aba_inserir(aba_inserir)
        self._montar_aba_excluir(aba_excluir)

    # ==========================================================
    # AUTOCOMPLETE (usado no campo de busca por título)
    # ==========================================================
    def _registrar_titulo_para_autocomplete(self, titulo):
        """Adiciona um título à lista usada pelo autocomplete, evitando
        duplicatas (mesmo título com acento/caixa diferente)."""
        chave = normalizar_titulo(titulo)
        if chave not in self._chaves_titulos_vistas:
            self._chaves_titulos_vistas.add(chave)
            self.titulos_unicos.append(titulo)

    def _ao_trocar_tipo_busca(self):
        self._esconder_sugestoes()

    def _ao_digitar_busca(self, evento):
        if evento.keysym in ("Down", "Up", "Return", "Escape"):
            return

        if self.tipo_busca.get() != "nome":
            self._esconder_sugestoes()
            return

        texto = self.entrada_busca.get().strip()
        if not texto:
            self._esconder_sugestoes()
            return

        alvo = normalizar_titulo(texto)

        # prioriza títulos que COMEÇAM com o texto digitado
        correspondentes = [
            t for t in self.titulos_unicos if normalizar_titulo(t).startswith(alvo)
        ]
        if not correspondentes:
            correspondentes = [
                t for t in self.titulos_unicos if alvo in normalizar_titulo(t)
            ]

        correspondentes = correspondentes[:8]

        if correspondentes:
            self._mostrar_sugestoes(correspondentes)
        else:
            self._esconder_sugestoes()

    def _mostrar_sugestoes(self, itens):
        self.lista_sugestoes.delete(0, tk.END)
        for item in itens:
            self.lista_sugestoes.insert(tk.END, item)
        self.lista_sugestoes.config(height=len(itens))
        x = self.entrada_busca.winfo_rootx() - self._aba_buscar.winfo_rootx()
        y = (
            self.entrada_busca.winfo_rooty()
            + self.entrada_busca.winfo_height()
            - self._aba_buscar.winfo_rooty()
        )
        largura = self.entrada_busca.winfo_width()

        self.lista_sugestoes.place(x=x, y=y, width=largura)
        self.lista_sugestoes.lift()

    def _esconder_sugestoes(self):
        if self.lista_sugestoes is not None:
            self.lista_sugestoes.place_forget()

    def _focar_sugestoes(self, evento):
        if self.lista_sugestoes is not None and self.lista_sugestoes.winfo_ismapped():
            self.lista_sugestoes.focus_set()
            self.lista_sugestoes.selection_clear(0, tk.END)
            self.lista_sugestoes.selection_set(0)
            self.lista_sugestoes.activate(0)
            return "break"

    def _selecionar_sugestao(self, evento=None):
        selecao = self.lista_sugestoes.curselection()
        if not selecao:
            return

        valor = self.lista_sugestoes.get(selecao[0])

        self.entrada_busca.delete(0, tk.END)
        self.entrada_busca.insert(0, valor)
        self._esconder_sugestoes()
        self.entrada_busca.focus_set()

        self._executar_busca()

    # ==========================================================
    # ABA: BUSCAR
    # ==========================================================
    def _montar_aba_buscar(self, aba):
        topo = ttk.Frame(aba, padding=10)
        topo.pack(fill="x")

        self.tipo_busca = tk.StringVar(value="nome")
        ttk.Radiobutton(
            topo,
            text="Por ID",
            variable=self.tipo_busca,
            value="id",
            command=self._ao_trocar_tipo_busca,
        ).pack(side="left")
        ttk.Radiobutton(
            topo,
            text="Por Título",
            variable=self.tipo_busca,
            value="nome",
            command=self._ao_trocar_tipo_busca,
        ).pack(side="left", padx=(8, 16))

        self.entrada_busca = ttk.Entry(topo, width=40)
        self.entrada_busca.pack(side="left", fill="x", expand=True)
        self.entrada_busca.bind("<Return>", lambda evento: self._executar_busca())
        self.entrada_busca.bind("<KeyRelease>", self._ao_digitar_busca)
        self.entrada_busca.bind("<Down>", self._focar_sugestoes)
        self.entrada_busca.bind("<Escape>", lambda evento: self._esconder_sugestoes())
        self.entrada_busca.bind(
            "<FocusOut>", lambda evento: self.after(150, self._esconder_sugestoes)
        )

        ttk.Button(topo, text="Buscar", command=self._executar_busca).pack(
            side="left", padx=(8, 0)
        )
        self._aba_buscar = aba
        self.lista_sugestoes = tk.Listbox(
            aba, activestyle="dotbox", exportselection=False, relief="solid", borderwidth=1
        )
        self.lista_sugestoes.bind("<<ListboxSelect>>", self._selecionar_sugestao)
        self.lista_sugestoes.bind("<Return>", self._selecionar_sugestao)
        self.lista_sugestoes.bind("<Escape>", lambda evento: self._esconder_sugestoes())

        self.label_desempenho = ttk.Label(
            aba, text="", padding=(10, 4), foreground="#205020"
        )
        self.label_desempenho.pack(fill="x")

        colunas = ("id", "titulo", "ano", "genero", "pais")
        self.tabela_resultados = ttk.Treeview(
            aba, columns=colunas, show="headings", height=16
        )
        titulos_coluna = {
            "id": "ID",
            "titulo": "Título",
            "ano": "Ano",
            "genero": "Gênero",
            "pais": "País",
        }
        larguras = {"id": 60, "titulo": 320, "ano": 60, "genero": 140, "pais": 160}
        for coluna in colunas:
            self.tabela_resultados.heading(coluna, text=titulos_coluna[coluna])
            self.tabela_resultados.column(coluna, width=larguras[coluna], anchor="w")

        self.tabela_resultados.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def _executar_busca(self):
        self._esconder_sugestoes()

        termo = self.entrada_busca.get().strip()
        if not termo:
            messagebox.showwarning("Atenção", "Digite algo para buscar.")
            return

        for linha in self.tabela_resultados.get_children():
            self.tabela_resultados.delete(linha)

        if self.tipo_busca.get() == "id":
            try:
                id_busca = int(termo)
            except ValueError:
                messagebox.showerror("Erro", "ID inválido: digite um número.")
                return

            inicio = time.perf_counter()
            filme_idx, comps_idx = buscar_por_id_comparacoes(
                self.blocos, self.indice, id_busca
            )
            tempo_idx = (time.perf_counter() - inicio) * 1000

            inicio = time.perf_counter()
            filme_seq, comps_seq = buscar_por_id_sequencial_comparacoes(
                self.filmes, id_busca
            )
            tempo_seq = (time.perf_counter() - inicio) * 1000

            self.label_desempenho.config(
                text=(
                    f"Indexada: {tempo_idx:.3f} ms, {comps_idx} comparações   |   "
                    f"Sequencial: {tempo_seq:.3f} ms, {comps_seq} comparações"
                )
            )

            filme = filme_idx or filme_seq
            if filme:
                self._inserir_linha_tabela(filme)
            else:
                messagebox.showinfo("Resultado", "Nenhum filme encontrado com esse ID.")

        else:
            inicio = time.perf_counter()
            resultados_seq, comps_seq = buscar_por_nome_sequencial_comparacoes(
                self.filmes, termo
            )
            tempo_seq = (time.perf_counter() - inicio) * 1000

            inicio = time.perf_counter()
            resultados_hash, ops_hash = buscar_por_hash_titulos_operacoes(
                self.hash_titulos, termo
            )
            tempo_hash = (time.perf_counter() - inicio) * 1000

            self.label_desempenho.config(
                text=(
                    f"Hash: {tempo_hash:.3f} ms, {ops_hash} operações   |   "
                    f"Sequencial: {tempo_seq:.3f} ms, {comps_seq} comparações"
                )
            )

            if resultados_hash:
                for filme in resultados_hash:
                    self._inserir_linha_tabela(filme)
            else:
                messagebox.showinfo(
                    "Resultado", "Nenhum filme encontrado com esse título."
                )

    def _inserir_linha_tabela(self, filme):
        self.tabela_resultados.insert(
            "",
            "end",
            values=(
                filme["id"],
                filme["Título da obra"],
                filme["Ano de exibição"],
                filme["Gênero"],
                filme["País(es) produtor(es) da obra"],
            ),
        )

    # ==========================================================
    # ABA: INSERIR
    # ==========================================================
    def _montar_aba_inserir(self, aba):
        container = ttk.Frame(aba, padding=16)
        container.pack(fill="both", expand=True)

        self.campos_entrada = {}

        for linha, (rotulo, chave_csv) in enumerate(CAMPOS_INSERIR):
            ttk.Label(container, text=rotulo + ":").grid(
                row=linha, column=0, sticky="w", pady=4, padx=(0, 8)
            )
            entrada = ttk.Entry(container, width=45)
            entrada.grid(row=linha, column=1, sticky="ew", pady=4)
            self.campos_entrada[chave_csv] = entrada

        container.columnconfigure(1, weight=1)

        ttk.Button(
            container, text="Inserir Filme", command=self._executar_insercao
        ).grid(row=len(CAMPOS_INSERIR), column=0, columnspan=2, pady=(16, 0))

    def _executar_insercao(self):
        valores = {}
        for chave_csv, entrada in self.campos_entrada.items():
            valores[chave_csv] = entrada.get().strip()

        if not valores["Título da obra"]:
            messagebox.showerror("Erro", "O título é obrigatório.")
            return

        try:
            valores["Ano de exibição"] = int(valores["Ano de exibição"])
        except ValueError:
            messagebox.showerror("Erro", "Ano inválido: digite um número.")
            return

        novo_id = max(f["id"] for f in self.filmes) + 1
        novo_filme = {"id": novo_id, **valores}

        self.filmes.append(novo_filme)
        inserir_filme(self.blocos, self.indice, novo_filme)
        self.hash_titulos.inserir(
            normalizar_titulo(novo_filme["Título da obra"]), novo_filme
        )
        self._registrar_titulo_para_autocomplete(novo_filme["Título da obra"])
        self.titulos_unicos.sort(key=normalizar_titulo)

        self.alteracoes_pendentes = True
        self.barra_status.config(
            text=f"{len(self.filmes)} filmes carregados  |  alterações não salvas"
        )

        for entrada in self.campos_entrada.values():
            entrada.delete(0, tk.END)

        messagebox.showinfo(
            "Sucesso", f"Filme '{novo_filme['Título da obra']}' inserido (ID {novo_id})."
        )

    # ==========================================================
    # ABA: EXCLUIR
    # ==========================================================
    def _montar_aba_excluir(self, aba):
        container = ttk.Frame(aba, padding=16)
        container.pack(fill="both", expand=True)

        self.tipo_exclusao = tk.StringVar(value="id")
        linha_topo = ttk.Frame(container)
        linha_topo.pack(fill="x")

        ttk.Radiobutton(
            linha_topo, text="Por ID", variable=self.tipo_exclusao, value="id"
        ).pack(side="left")
        ttk.Radiobutton(
            linha_topo, text="Por Título", variable=self.tipo_exclusao, value="nome"
        ).pack(side="left", padx=(8, 16))

        self.entrada_exclusao = ttk.Entry(linha_topo, width=40)
        self.entrada_exclusao.pack(side="left", fill="x", expand=True)

        ttk.Button(
            linha_topo, text="Buscar para excluir", command=self._preparar_exclusao
        ).pack(side="left", padx=(8, 0))

        colunas = ("id", "titulo", "ano")
        self.lista_exclusao = ttk.Treeview(
            container, columns=colunas, show="headings", height=12, selectmode="browse"
        )
        for coluna, rotulo, largura in (
            ("id", "ID", 60),
            ("titulo", "Título", 380),
            ("ano", "Ano", 60),
        ):
            self.lista_exclusao.heading(coluna, text=rotulo)
            self.lista_exclusao.column(coluna, width=largura, anchor="w")
        self.lista_exclusao.pack(fill="both", expand=True, pady=10)

        ttk.Button(
            container,
            text="Excluir filme selecionado",
            command=self._executar_exclusao,
        ).pack()

        self._candidatos_exclusao = {}

    def _preparar_exclusao(self):
        termo = self.entrada_exclusao.get().strip()
        if not termo:
            messagebox.showwarning("Atenção", "Digite um ID ou título.")
            return

        for linha in self.lista_exclusao.get_children():
            self.lista_exclusao.delete(linha)
        self._candidatos_exclusao = {}

        if self.tipo_exclusao.get() == "id":
            try:
                id_busca = int(termo)
            except ValueError:
                messagebox.showerror("Erro", "ID inválido: digite um número.")
                return
            encontrados = [f for f in self.filmes if f["id"] == id_busca]
        else:
            encontrados = buscar_por_nome_sequencial(self.filmes, termo)

        if not encontrados:
            messagebox.showinfo("Resultado", "Nenhum filme encontrado.")
            return

        for filme in encontrados:
            item_id = self.lista_exclusao.insert(
                "", "end", values=(filme["id"], filme["Título da obra"], filme["Ano de exibição"])
            )
            self._candidatos_exclusao[item_id] = filme

    def _executar_exclusao(self):
        selecionado = self.lista_exclusao.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um filme na lista.")
            return

        filme = self._candidatos_exclusao.get(selecionado[0])
        if filme is None:
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            f"Excluir '{filme['Título da obra']}' (ID {filme['id']})?",
        )
        if not confirmar:
            return

        self.filmes.remove(filme)
        excluir_filme(self.blocos, self.indice, filme["id"])

        self.lista_exclusao.delete(selecionado[0])
        del self._candidatos_exclusao[selecionado[0]]

        self.alteracoes_pendentes = True
        self.barra_status.config(
            text=f"{len(self.filmes)} filmes carregados  |  alterações não salvas"
        )

        messagebox.showinfo("Sucesso", "Filme excluído.")

    # ==========================================================
    # FECHAMENTO / SALVAMENTO
    # ==========================================================
    def _ao_fechar(self):
        if self.alteracoes_pendentes:
            salvar = messagebox.askyesnocancel(
                "Salvar alterações",
                "Há alterações não salvas. Deseja salvar no CSV antes de sair?",
            )
            if salvar is None:
                return
            if salvar:
                salvar_csv(self.caminho_csv, self.filmes)
        self.destroy()


if __name__ == "__main__":
    app = AppFilmes()
    app.mainloop()