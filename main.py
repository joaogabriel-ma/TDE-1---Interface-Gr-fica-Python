"""
Aplicativo de Lista de Tarefas - Kivy
TDE 1 - Interface Gráfica em Python

Para executar:
    pip install kivy
    python main.py
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition

from estilo import FUNDO
from tela_lista import TelaLista
from tela_adicionar import TelaAdicionar

# Tamanho de janela parecido com um celular (facilita a demonstração no desktop)
Window.size = (420, 720)
# Cor de fundo da janela (tema escuro)
Window.clearcolor = FUNDO


class ListaTarefasApp(App):
    """Classe principal: o Kivy chama build() ao iniciar e usa o retorno como raiz."""

    title = "Lista de Tarefas"

    def build(self):
        # Armazenamento em memória: lista de dicionários, sem banco e sem arquivo.
        # Formato de cada tarefa:
        # {"titulo": str, "descricao": str, "concluida": bool}
        tarefas = []

        # O ScreenManager controla qual tela está visível e anima a troca.
        gerenciador = ScreenManager(transition=SlideTransition())

        # A MESMA lista é passada para as duas telas (é compartilhada por referência)
        gerenciador.add_widget(TelaLista(tarefas=tarefas, name="lista"))
        gerenciador.add_widget(TelaAdicionar(tarefas=tarefas, name="adicionar"))

        return gerenciador


if __name__ == "__main__":
    ListaTarefasApp().run()
