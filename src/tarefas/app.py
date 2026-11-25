from flask import Flask, redirect, render_template, request, url_for

from tarefas.models.database import init_db
from tarefas.models.tarefa import Tarefa

app = Flask(__name__)

with app.app_context():
    init_db()

@app.route('/test')
def test():
    return 'Servidor Online!'                                                   

@app.route('/', methods=['GET', 'POST'])
def home():

    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa']
        data_conclusao_form = request.form['dataConclusao']

        data_corrigida = data_conclusao_form or None

        tarefa = Tarefa(titulo=titulo_form, data_conclusao=data_corrigida)

        # Salvamos a tarefa no banco
        tarefa.salvarTarefa()

        return redirect(url_for('home'))

    tarefas= Tarefa.listarTarefas()

    return render_template(
        'base.html',
        titulo_da_pagina='Minha lista', 
        tarefas_da_pagina=tarefas,
        button_submit="Adicionar",
        mostrar_voltar=False,
        mostrar_lista=True,
    )

@app.route('/delete/<int:id_tarefa>')
def apagar_id_especificado(id_tarefa):
    Tarefa.apagarTarefas(id_tarefa)
    return redirect(url_for('home'))



@app.route('/edit/<int:id_tarefa>', methods=['GET', 'POST']) 
def editar_id_especificado(id_tarefa):

    if request.method == 'POST':
        titulo_form = request.form['tituloTarefa']
        data_conclusao_form = request.form['dataConclusao']

        data_corrigida = data_conclusao_form or None

        tarefa = Tarefa(
            titulo=titulo_form,
            id=id_tarefa,
            data_conclusao=data_corrigida
        )

        tarefa.editarTarefas()

        return redirect(url_for('home'))

    tarefa_selecionada = Tarefa.carregar_tarefa(id_tarefa
                                                )
    return render_template(
        "base.html",
        titulo_da_pagina="Minha lista de tarefas",
        tarefas_da_pagina=[],
        button_submit="Atualizar",
        mostrar_voltar=True,
        mostrar_lista=False,
        tarefa_edicao = tarefa_selecionada

    )
if __name__ == '__main__':

    app.run()