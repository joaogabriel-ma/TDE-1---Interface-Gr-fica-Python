"""
Tela 1 - Exibir tarefas cadastradas.

- Lista título e status de cada tarefa (em cartões arredondados)
- Permite marcar como concluída direto na lista (CheckBox)
- Concluídas: título riscado e status verde | Pendentes: status laranja
- Botão para navegar até a Tela 2 (Adicionar Tarefa)
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import Screen
from kivy.utils import escape_markup

from estilo import (Cartao, BotaoArredondado, DESTAQUE, TEXTO, TEXTO_SUAVE,
                    HEX_PENDENTE, HEX_CONCLUIDA, HEX_SUAVE)


class TelaLista(Screen):
    """Tela que mostra todas as tarefas cadastradas."""

    def __init__(self, tarefas, **kwargs):
        super().__init__(**kwargs)
        self.tarefas = tarefas  # lista de dicionários compartilhada com a Tela 2

        # Layout raiz da tela: componentes empilhados na vertical
        raiz = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        # Cabeçalho: título + resumo (ex: "2 pendentes · 1 concluída")
        cabecalho = BoxLayout(orientation="vertical", size_hint_y=None, height=dp(70))
        cabecalho.add_widget(
            Label(text="Minhas Tarefas", font_size="28sp", bold=True, color=TEXTO,
                  halign="left", valign="middle")
        )
        self.resumo = Label(text="", font_size="14sp", color=TEXTO_SUAVE,
                            halign="left", valign="middle")
        cabecalho.add_widget(self.resumo)
        for filho in cabecalho.children:  # alinha os textos à esquerda
            filho.bind(size=lambda inst, tam: setattr(inst, "text_size", tam))
        raiz.add_widget(cabecalho)

        # ScrollView permite rolar a lista quando houver muitas tarefas
        rolagem = ScrollView(bar_width=dp(3))

        # GridLayout de 1 coluna: cada linha é uma tarefa.
        # size_hint_y=None + minimum_height faz o grid crescer conforme o conteúdo.
        self.container = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        self.container.bind(minimum_height=self.container.setter("height"))
        rolagem.add_widget(self.container)
        raiz.add_widget(rolagem)

        # Botão que leva para a Tela 2
        botao_nova = BotaoArredondado(text="+ Nova tarefa", size_hint_y=None, height=dp(56))
        botao_nova.bind(on_release=self.ir_para_adicionar)
        raiz.add_widget(botao_nova)

        self.add_widget(raiz)

    def on_pre_enter(self, *args):
        """Evento do Screen: roda sempre que a tela está prestes a aparecer.
        Garante que tarefas recém-adicionadas na Tela 2 apareçam aqui."""
        self.atualizar_lista()

    def atualizar_lista(self):
        """Reconstrói as linhas da lista a partir da lista em memória."""
        self.container.clear_widgets()

        if not self.tarefas:
            self.container.add_widget(
                Label(text="Nenhuma tarefa ainda.\nToque em \"+ Nova tarefa\" para começar.",
                      color=TEXTO_SUAVE, halign="center", size_hint_y=None, height=dp(120))
            )
        else:
            for tarefa in self.tarefas:
                self.container.add_widget(self.criar_linha(tarefa))

        self.atualizar_resumo()

    def atualizar_resumo(self):
        """Atualiza o contador de tarefas pendentes e concluídas."""
        concluidas = sum(1 for t in self.tarefas if t["concluida"])
        pendentes = len(self.tarefas) - concluidas
        self.resumo.text = f"{pendentes} pendente(s)  ·  {concluidas} concluída(s)"

    def criar_linha(self, tarefa):
        """Cria o cartão visual (CheckBox + texto) de uma tarefa."""
        linha = Cartao(orientation="horizontal", size_hint_y=None, height=dp(80),
                       padding=[dp(8), dp(8), dp(12), dp(8)], spacing=dp(6))

        # color=DESTAQUE pinta o checkbox com a cor do tema
        checkbox = CheckBox(active=tarefa["concluida"], size_hint_x=None,
                            width=dp(48), color=DESTAQUE)

        # markup=True permite cor, negrito e riscado dentro do texto
        rotulo = Label(markup=True, halign="left", valign="middle", color=TEXTO)
        # Faz o texto quebrar linha e alinhar à esquerda dentro do Label
        rotulo.bind(size=lambda inst, tam: setattr(inst, "text_size", tam))

        def atualizar_texto():
            """Monta o texto conforme o status atual da tarefa."""
            titulo = escape_markup(tarefa["titulo"])  # evita que [ ] do usuário quebrem o markup
            descricao = escape_markup(tarefa["descricao"])

            if tarefa["concluida"]:
                texto = (f"[color={HEX_SUAVE}][s]{titulo}[/s][/color]\n"
                         f"[size=13sp][color={HEX_CONCLUIDA}]Concluída[/color][/size]")
            else:
                texto = (f"[b]{titulo}[/b]\n"
                         f"[size=13sp][color={HEX_PENDENTE}]Pendente[/color][/size]")

            if descricao:
                texto += f"\n[size=12sp][color={HEX_SUAVE}]{descricao}[/color][/size]"
            rotulo.text = texto

        def ao_marcar(instancia, marcado):
            """Evento on_active do CheckBox: atualiza o dicionário e o visual."""
            tarefa["concluida"] = marcado
            atualizar_texto()
            self.atualizar_resumo()

        checkbox.bind(active=ao_marcar)
        atualizar_texto()

        linha.add_widget(checkbox)
        linha.add_widget(rotulo)
        return linha

    def ir_para_adicionar(self, *args):
        """Navega para a Tela 2 trocando a tela atual do ScreenManager."""
        self.manager.transition.direction = "left"
        self.manager.current = "adicionar"
