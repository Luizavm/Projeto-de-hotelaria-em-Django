from flask import Flask, render_template, redirect, flash, request, url_for 
import os
from werkzeug.utils import secure_filename
import csv
from datetime import datetime

app = Flask(__name__)

# Define os caminhos dos arquivos CSV
csv_projetos = "projetos.csv"
csv_tarefas = "tarefas.csv"

app.secret_key = os.urandom(24).hex()

context = {}

# Dicionários em memória
projetos = {}
tarefas_por_projeto = {}

# Função para ler os dados dos CSVs (para manter os dados persistentes)
def carregar_dados_csv():
    # Carregar projetos do CSV
    if os.path.exists(csv_projetos):
        with open(csv_projetos, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_projeto = int(row["id"])
                projetos[id_projeto] = {
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "imagem": row["imagem"],
                    "data_criacao": row["data_criacao"]
                }
                
    # Carregar tarefas do CSV
    if os.path.exists(csv_tarefas):
        with open(csv_tarefas, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                id_projeto = int(row["id_projeto"])
                tarefa = {
                    "id": int(row["id"]),
                    "id_projeto": id_projeto,
                    "nome": row["nome"],
                    "descricao": row["descricao"],
                    "status": row["status"]
                }
                if id_projeto not in tarefas_por_projeto:
                    tarefas_por_projeto[id_projeto] = []
                tarefas_por_projeto[id_projeto].append(tarefa)

# Funções para salvar os dados em CSV
def salvar_projetos_csv():
    with open(csv_projetos, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "nome", "descricao", "imagem", "data_criacao"])
        for id, projeto in projetos.items():
            writer.writerow([id, projeto["nome"], projeto["descricao"], projeto["imagem"], projeto["data_criacao"]])

def salvar_tarefas_csv():
    with open(csv_tarefas, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "id_projeto", "nome", "descricao", "status"])
        for lista in tarefas_por_projeto.values():
            for tarefa in lista:
                writer.writerow([tarefa["id"], tarefa["id_projeto"], tarefa["nome"], tarefa["descricao"], tarefa["status"]])

# Carregar os dados do CSV quando o app inicia
carregar_dados_csv()

# Home
@app.route('/')
def homepage():
    context["Inicio"] = "img/imginicio.jpg"
    context["Titulo"] = "Luiz Projeto"
    context["Texto"] = '''Gerenciador de projetos'''
    return render_template("homepage.html", **context)

# Exibe todos os projetos
@app.route('/projetos')
def lista_projetos():
    context["projetos"] = projetos
    return render_template("lista_projetos.html", **context)

# Formulário para adicionar projeto
@app.route('/add_projeto_form')
def add_projeto_form():
    return render_template('add_projeto.html', **context)

# Adiciona projeto
@app.route('/add_projeto', methods=['POST'])
def add_projeto():
    next_id = max(projetos.keys(), default=0) + 1
    nome = request.form['nome']
    descricao = request.form['descricao']
    imagem = request.files['imagem']
    imagem_path = None
    if imagem:
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join('static/img', filename))
        imagem_path = f'img/{filename}'
    data_criacao = datetime.now().strftime("%Y-%m-%d")
    projetos[next_id] = {
        "nome": nome,
        "descricao": descricao,
        "imagem": imagem_path,
        "data_criacao": data_criacao
    }
    tarefas_por_projeto[next_id] = []
    salvar_projetos_csv()
    return redirect(url_for('lista_projetos'))

# Editar projeto
@app.route('/edit_projeto/<int:id>', methods=['GET'])
def edit_projeto(id):
    projeto = projetos.get(id)
    if not projeto:
        flash("Projeto não encontrado.", "error")
        return redirect(url_for('lista_projetos.html'))
    
    return render_template("edit_projeto.html", projeto=projeto, id=id)

@app.route('/up_projeto', methods=['POST'])
def up_projeto():
    projeto_id = int(request.form.get('id'))
    nome = request.form.get('nome')
    descricao = request.form.get('descricao')
    imagem = request.files.get('imagem')

    projeto = projetos.get(projeto_id)
    if not projeto:
        flash("Projeto não encontrado.", "error")
        return redirect(url_for('lista_projetos.html'))

    # Atualiza os dados
    projeto["nome"] = nome
    projeto["descricao"] = descricao
    if imagem and imagem.filename:
        filename = secure_filename(imagem.filename)
        imagem.save(os.path.join('static/img', filename))
        projeto["imagem"] = f'img/{filename}'

    salvar_projetos_csv()
    return redirect(url_for('ver_projeto', id=projeto_id))

# Visualiza tarefas de um projeto
@app.route('/projeto/<int:id>')
def ver_projeto(id):
    projeto = projetos.get(id)
    tarefas = tarefas_por_projeto.get(id, [])
    if not projeto:
        flash("Projeto não encontrado.", "error")
        return redirect(url_for('lista_projetos'))
    return render_template("projeto_tarefas.html", projeto=projeto, tarefas=tarefas, id=id)

# Adiciona tarefa a um projeto
@app.route('/add_tarefa/<int:id_projeto>', methods=['GET', 'POST'])
def add_tarefa(id_projeto):
    if id_projeto not in projetos:
        flash("Projeto não encontrado.", "error")
        return redirect(url_for('lista_projetos'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        status = request.form['status']
        next_id = sum(len(lst) for lst in tarefas_por_projeto.values()) + 1
        tarefa = {
            "id": next_id,
            "id_projeto": id_projeto,
            "nome": nome,
            "descricao": descricao,
            "status": status  # Aqui o status da tarefa será salvo
        }
        
        # Verifica se o projeto já tem tarefas associadas, caso contrário, inicializa a lista
        if id_projeto not in tarefas_por_projeto:
            tarefas_por_projeto[id_projeto] = []
        
        tarefas_por_projeto[id_projeto].append(tarefa)
        salvar_tarefas_csv()
        return redirect(url_for('ver_projeto', id=id_projeto))

    return render_template("add_tarefa.html", id_projeto=id_projeto)

@app.route('/edit_tarefa/<int:id_projeto>/<int:id_tarefa>', methods=['GET', 'POST'])
def edit_tarefa(id_projeto, id_tarefa):
    # Encontrar a tarefa com base no id_projeto e id_tarefa
    tarefa = next((t for t in tarefas_por_projeto.get(id_projeto, []) if t["id"] == id_tarefa), None)
    
    if not tarefa:
        flash("Tarefa não encontrada.", "error")
        return redirect(url_for('ver_projeto', id=id_projeto))

    if request.method == 'POST':
        # Atualizar os campos da tarefa
        tarefa["nome"] = request.form['nome']
        tarefa["descricao"] = request.form['descricao']
        tarefa["status"] = request.form['status']
        salvar_tarefas_csv()  # Salvar as alterações no CSV
        return redirect(url_for('ver_projeto', id=id_projeto))

    return render_template("edit_tarefa.html", tarefa=tarefa, id_projeto=id_projeto, id_tarefa=id_tarefa)

# Deleta projeto e tarefas associadas
@app.route('/delete_projeto/<int:id>', methods=['POST'])
def delete_projeto(id):
    if id in projetos:
        projetos.pop(id)
        tarefas_por_projeto.pop(id, None)
        salvar_projetos_csv()
        salvar_tarefas_csv()
        flash("Projeto e tarefas excluídos.", "success")
    else:
        flash("Projeto não encontrado.", "error")
    return redirect(url_for('lista_projetos'))

# Deleta tarefa (nova rota)
@app.route('/delete_tarefa/<int:id_projeto>/<int:id_tarefa>', methods=['POST'])
def delete_tarefa(id_projeto, id_tarefa):
    tarefa = next((t for t in tarefas_por_projeto.get(id_projeto, []) if t["id"] == id_tarefa), None)
    if tarefa:
        tarefas_por_projeto[id_projeto].remove(tarefa)
        salvar_tarefas_csv()
        flash("Tarefa excluída.", "success")
    else:
        flash("Tarefa não encontrada.", "error")
    return redirect(url_for('ver_projeto', id=id_projeto))

# Excluir projetos
@app.route('/excluir_projetos')
def excluir_projetos():
    context["projetos"] = projetos
    return render_template("excluir_projetos.html", **context)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
