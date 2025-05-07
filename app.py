
from flask import Flask, request, render_template, redirect, url_for
import dateparser
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

thoughts = []
historico = []

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        thought = request.form['thought']
        date = dateparser.parse(thought)
        thoughts.append({"text": thought, "date": date.strftime('%d/%m/%Y') if date else ""})
        return redirect(url_for('index'))
    return render_template('index.html', thoughts=thoughts)

@app.route('/zen')
def zen_mode():
    return render_template('zen.html')

@app.route('/historico')
def historico_page():
    return render_template('historico.html', historico=historico)

@app.route('/grafico')
def grafico_page():
    categorias = {}
    for item in thoughts:
        categoria = "Outros"
        if "comprar" in item['text'].lower():
            categoria = "Compras"
        elif "pagar" in item['text'].lower():
            categoria = "Contas"
        categorias[categoria] = categorias.get(categoria, 0) + 1

    plt.clf()
    plt.pie(categorias.values(), labels=categorias.keys(), autopct='%1.1f%%')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    grafico_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return render_template('grafico.html', grafico_base64=grafico_base64)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
