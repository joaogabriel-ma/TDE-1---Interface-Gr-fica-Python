▶️ Como rodar o app Lista de Tarefas (Kivy)

⚠️ IMPORTANTE: use o Python 3.12. Nas versões 3.13 e 3.14 o Kivy não instala.

1) Baixar o projeto
No GitHub, clique no botão verde "Code" > "Download ZIP" e extraia a pasta.
(Ou, se usa git: git clone <link-do-repositorio>)

2) Instalar o Python 3.12 (se ainda não tiver)
Baixe o "Windows installer (64-bit)" do Python 3.12.10 em:
https://www.python.org/downloads/release/python-31210/
Na instalação, marque "Add python.exe to PATH" e clique em "Install Now".
Para conferir, abra o terminal e digite: py -3.12 --version

3) Abrir o terminal dentro da pasta do projeto
No VS Code: File > Open Folder (escolha a pasta) e depois Terminal > New Terminal.
Ou no Windows: abra a pasta, clique na barra de endereço, digite cmd e dê Enter.

4) Instalar o Kivy (só na primeira vez)
py -3.12 -m pip install kivy

5) Rodar o app
py -3.12 main.py

Pronto: a janela da Lista de Tarefas deve abrir. ✅
