"""
Estilo visual do app: paleta de cores e componentes reutilizáveis.
Centralizar o visual aqui deixa as telas mais limpas e fáceis de explicar.
"""

from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

# Paleta (tema escuro). No Kivy, uma cor é (R, G, B, A) com valores de 0 a 1.
FUNDO = (0.07, 0.07, 0.11, 1)
CARTAO = (0.13, 0.13, 0.20, 1)
DESTAQUE = (0.42, 0.39, 1.00, 1)   # roxo/azulado
CINZA = (0.25, 0.25, 0.33, 1)
TEXTO = (0.95, 0.95, 0.98, 1)
TEXTO_SUAVE = (0.60, 0.60, 0.70, 1)
ERRO = (1.00, 0.40, 0.40, 1)

# Cores em hexadecimal, usadas dentro do markup dos textos
HEX_PENDENTE = "ffa726"   # laranja
HEX_CONCLUIDA = "66bb6a"  # verde
HEX_SUAVE = "8a8a99"      # cinza


class Cartao(BoxLayout):
    """BoxLayout com fundo de cantos arredondados (usado em cada tarefa)."""

    def __init__(self, cor=CARTAO, **kwargs):
        super().__init__(**kwargs)
        # canvas.before desenha ANTES dos widgets filhos, ou seja, como fundo
        with self.canvas.before:
            Color(*cor)
            self._fundo = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])
        # Quando o cartão muda de posição/tamanho, o fundo acompanha
        self.bind(pos=self._atualizar, size=self._atualizar)

    def _atualizar(self, *args):
        self._fundo.pos = self.pos
        self._fundo.size = self.size


class BotaoArredondado(Button):
    """Botão colorido com cantos arredondados e efeito ao pressionar."""

    def __init__(self, cor=DESTAQUE, **kwargs):
        super().__init__(**kwargs)
        # Remove o visual padrão do Kivy (imagem cinza) e deixa só o nosso desenho
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.bold = True
        self.font_size = "16sp"
        self.cor = cor

        with self.canvas.before:
            self._cor_fundo = Color(*cor)
            self._fundo = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(14)])

        self.bind(pos=self._atualizar, size=self._atualizar,
                  on_press=self._escurecer, on_release=self._restaurar)

    def _atualizar(self, *args):
        self._fundo.pos = self.pos
        self._fundo.size = self.size

    def _escurecer(self, *args):
        """Feedback visual: escurece a cor enquanto o botão está pressionado."""
        r, g, b, _ = self.cor
        self._cor_fundo.rgba = (r * 0.7, g * 0.7, b * 0.7, 1)

    def _restaurar(self, *args):
        self._cor_fundo.rgba = self.cor


def estilizar_campo(campo):
    """Aplica o tema escuro a um TextInput."""
    campo.background_normal = ""
    campo.background_active = ""
    campo.background_color = CARTAO
    campo.foreground_color = TEXTO
    campo.hint_text_color = TEXTO_SUAVE
    campo.cursor_color = DESTAQUE
    campo.padding = [dp(14), dp(14), dp(14), dp(14)]
    return campo
