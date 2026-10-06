"""
Tela 2 - Adicionar tarefa.

- Campo de texto para o título (obrigatório)
- Campo de texto para a descrição (opcional)
- Salvar: insere na lista em memória e volta para a Tela 1
- Cancelar: descarta e volta para a Tela 1
- Validação: não permite salvar com título vazio
"""

from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.textinput import TextInput

from estilo import BotaoArredondado, estilizar_campo, TEXTO, TEXTO_SUAVE, ERRO, CINZA, DESTAQUE


class TelaAdicionar(Screen):
    """Tela com o formulário de nova tarefa."""

    def __init__(self, tarefas, **kwargs):
        super().__init__(**kwargs)
        self.tarefas = tarefas  # mesma lista usada pela Tela 1

        raiz = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(12))

        titulo_tela = Label(text="Nova Tarefa", font_size="28sp", bold=True, color=TEXTO,
                            halign="left", valign="middle", size_hint_y=None, height=dp(60))
        titulo_tela.bind(size=lambda inst, tam: setattr(inst, "text_size", tam))
        raiz.add_widget(titulo_tela)

        # Campo do título: multiline=False => uma linha só
        self.campo_titulo = estilizar_campo(TextInput(
            hint_text="Título da tarefa (obrigatório)",
            multiline=False, size_hint_y=None, height=dp(52),
        ))
        raiz.add_widget(self.campo_titulo)

        # Campo da descrição: multiline=True => aceita várias linhas
        self.campo_descricao = estilizar_campo(TextInput(
            hint_text="Descrição / detalhes (opcional)", multiline=True,
        ))
        raiz.add_widget(self.campo_descricao)

        # Label usado para mostrar a mensagem de erro da validação
        self.mensagem_erro = Label(text="", color=ERRO, size_hint_y=None, height=dp(30))
        raiz.add_widget(self.mensagem_erro)

        # Linha com os dois botões lado a lado
        botoes = BoxLayout(orientation="horizontal", spacing=dp(12),
                           size_hint_y=None, height=dp(56))

        botao_cancelar = BotaoArredondado(text="Cancelar", cor=CINZA)
        botao_cancelar.bind(on_release=self.cancelar)

        botao_salvar = BotaoArredondado(text="Salvar", cor=DESTAQUE)
        botao_salvar.bind(on_release=self.salvar)

        botoes.add_widget(botao_cancelar)
        botoes.add_widget(botao_salvar)
        raiz.add_widget(botoes)

        self.add_widget(raiz)

    def on_pre_enter(self, *args):
        """Sempre que a tela abre, o formulário começa limpo."""
        self.limpar_campos()

    def limpar_campos(self):
        self.campo_titulo.text = ""
        self.campo_descricao.text = ""
        self.mensagem_erro.text = ""

    def salvar(self, *args):
        """Valida o título, grava a tarefa na lista em memória e volta."""
        titulo = self.campo_titulo.text.strip()  # strip() trata "   " como vazio

        # Validação básica: título não pode ser vazio
        if not titulo:
            self.mensagem_erro.text = "O título não pode ficar vazio!"
            return

        self.tarefas.append({
            "titulo": titulo,
            "descricao": self.campo_descricao.text.strip(),
            "concluida": False,
        })
        self.voltar_para_lista()

    def cancelar(self, *args):
        """Descarta o que foi digitado e volta para a Tela 1."""
        self.voltar_para_lista()

    def voltar_para_lista(self):
        self.manager.transition.direction = "right"
        self.manager.current = "lista"
