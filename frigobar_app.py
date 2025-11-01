from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

# Data structure to store items and prices
ITEMS = {
    "beverages": [
        {"name": "Água Mineral s/Gás (500ml)", "price": 8, "icon": "agua.ico", "quantity": 0},
        {"name": "Água Mineral c/Gás (310ml)", "price": 8, "icon": "aguacomgas.ico", "quantity": 0},
        {"name": "Coca-cola (lata 350ml)", "price": 9, "icon": "cocacola.ico", "quantity": 0},
        {"name": "Fanta (lata 350ml)", "price": 9, "icon": "fanta.ico", "quantity": 0},
        {"name": "Guaraná (lata 350ml)", "price": 9, "icon": "guarana.ico", "quantity": 0},
        {"name": "Toddynho (200ml)", "price": 10, "icon": "toddynho.ico", "quantity": 0},
        {"name": "Antarctica (lata 350ml)", "price": 12, "icon": "antarctica.ico", "quantity": 0}
    ],
    "snacks": [
        {"name": "Castanha de Caju (50g)", "price": 17, "icon": "castanhadecaju.ico", "quantity": 0},
        {"name": "Batata (40g)", "price": 11, "icon": "batata.ico", "quantity": 0},
        {"name": "Chocolate Kit Kat (41,5g)", "price": 10, "icon": "kitkat.ico", "quantity": 0},
        {"name": "Bala Mentos crazyfruit (41,5g)", "price": 8, "icon": "mentoscrazyfruit.ico", "quantity": 0},
        {"name": "Bala Mentos mint (41,5g)", "price": 8, "icon": "mentosmint.ico", "quantity": 0}
    ]
}

# Generate apartment data
APARTMENTS = []
for floor in range(3, 11):
    room_count = 7 if floor == 10 else 8
    for room in range(1, room_count + 1):
        apartment = f"100{room}" if floor == 10 else f"{floor}0{room}"
        APARTMENTS.append(apartment)

@app.route('/')
def index():
    return render_template('index.html', items=ITEMS, apartments=APARTMENTS)

@app.route('/update_quantity', methods=['POST'])
def update_quantity():
    data = request.json
    category = data.get('category')
    item_index = data.get('item_index')
    action = data.get('action')  # 'add' or 'remove'
    
    if category in ITEMS and 0 <= item_index < len(ITEMS[category]):
        if action == 'add':
            ITEMS[category][item_index]['quantity'] += 1
        elif action == 'remove' and ITEMS[category][item_index]['quantity'] > 0:
            ITEMS[category][item_index]['quantity'] -= 1
    
    return jsonify({
        'quantity': ITEMS[category][item_index]['quantity'],
        'total': ITEMS[category][item_index]['quantity'] * ITEMS[category][item_index]['price'],
        'summary': calculate_summary()
    })

@app.route('/reset', methods=['POST'])
def reset():
    for category in ITEMS:
        for item in ITEMS[category]:
            item['quantity'] = 0
    return jsonify({'success': True})

def calculate_summary():
    total_beverages = sum(item['quantity'] * item['price'] for item in ITEMS['beverages'])
    total_snacks = sum(item['quantity'] * item['price'] for item in ITEMS['snacks'])
    total_cost = total_beverages + total_snacks
    
    return {
        'total_beverages': total_beverages,
        'total_snacks': total_snacks,
        'total_cost': total_cost
    }

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Write the HTML template
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <link rel="manifest" href="manifest.json">
    <link rel="icon" href="logo.ico" type="image/ico">
    <link rel="apple-touch-icon" sizes="192x192" href="logo.ico">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="application-name" content="Frigobar">
    <meta name="theme-color" content="#ffffff"> 
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frigobar</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            color: #333;
        }

        .container {
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: relative; /* Para posicionar o botão de instalação */
        }

        h1, h2 {
            color: #2c3e50;
            text-align: center;
        }

        .apartment-list {
            display: none; /* Inicialmente oculto */
            margin-top: 20px;
        }

        .floor {
            margin-bottom: 20px;
        }

        .apartment {
            background: #007bff;
            color: white;
            padding: 8px;
            text-align: center;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s;
            margin: 5px;
            font-size: 12px;
            display: inline-block;
            width: calc(25% - 10px);
        }

        .apartment:hover {
            background: #0056b3;
        }

        .item-container {
            margin-bottom: 20px;
        }

        .item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #ecf0f1;
            transition: background-color 0.3s;
        }

        .item:hover {
            background-color: #dfe6e9;
        }

        .item button {
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .item button.remove {
            background-color: #e74c3c;
        }

        .item button:hover {
            background-color: #2980b9;
        }

        .item button.remove:hover {
            background-color: #c0392b;
        }

        .quantity, .total {
            margin-left: 10px;
            font-weight: bold;
        }

        #summary {
            margin-top: 20px;
            font-size: 1.2em;
            text-align: center;
        }

        .input-apartment {
            margin-bottom: 20px;
            text-align: center;
        }

        .input-apartment input {
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: calc(100% - 22px);
            max-width: 300px;
        }

        button.send-whatsapp {
            background-color: #25D366;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            display: block;
            margin: 20px auto;
            transition: background-color 0.3s;
        }

        button.send-whatsapp:hover {
            background-color: #1da851;
        }

        h5 {
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
        }

        .install-button {
            background: #4CAF50;
            color: white;
            padding: 10px;
            border: none;
            border-radius: 50%; /* Faz o botão redondo */
            cursor: pointer;
            position: absolute; /* Posiciona-o absolutamente */
            top: 20px; /* Distância do topo */
            left: 20px; /* Distância da esquerda */
            width: 40px; /* Largura fixa */
            height: 40px; /* Altura fixa */
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background-color 0.3s;
        }

        .install-button:hover {
            background-color: #45a049;
        }

        #show-apartments {
            background-color: blue; /* Cor do botão azul */
            color: white; /* Cor do texto branco */
            border: none; /* Remove a borda */
            padding: 10px 20px; /* Adiciona padding */
            font-size: 16px; /* Define o tamanho da fonte */
            cursor: pointer; /* Muda o cursor para pointer */
            border-radius: 5px; /* Adiciona borda arredondada */
            display: block; /* Faz do botão um elemento de bloco */
            margin: 20px auto; /* Centraliza o botão */
        }
    </style>
</head>
<body>

    <!-- Modal de Confirmação -->
<div id="confirmationModal" style="display: none;">
    <div class="modal-content">
        <p>Foi saída ou arrumação?</p>
        <button id="confirmExit">Saída</button>
        <button id="confirmCleaning">Arrumação</button>
    </div>
</div>

<style>
    /* Estilos do Modal */
    #confirmationModal {
        position: fixed;
        z-index: 1000;
        left: 0;
        top: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
        display: flex;
        justify-content: center;
        align-items: center;
    }

    .modal-content {
        background: white;
        padding: 20px;
        border-radius: 5px;
        text-align: center;
    }

    button {
        margin: 5px;
        padding: 10px 20px;
        border: none;
        border-radius: 5px;
        cursor: pointer;
    }
</style>

    <div class="container">
        <h1>Frigobar</h1>

        <div class="input-apartment">
            <label for="apartmentNumber"><strong>Número do Apartamento:</strong></label>
            <input type="text" id="apartmentNumber" placeholder="Digite o número do apartamento" />
        </div>

        <button id="show-apartments">Selecionar Apartamentos</button> <!-- Botão centralizado -->

        <div class="apartment-list" id="apartment-list">
            <!-- Apartamentos serão gerados aqui -->
        </div>

        <h2>Bebidas</h2>
        <div class="item-container" id="beverages">
            {% for item in items.beverages %}
            <div class="item" id="beverage-{{ loop.index0 }}">
                <img src="{{ item.icon }}" alt="{{ item.name }}" style="width: 50px; cursor: pointer;" onclick="addItem('beverages', {{ loop.index0 }})">
                <span>{{ item.name }}</span>
                <button class="remove" onclick="removeItem('beverages', {{ loop.index0 }})">Remover</button>
                <span class="quantity" id="quantity-beverages-{{ loop.index0 }}">0</span>
                <span class="total" id="total-beverages-{{ loop.index0 }}">0</span>
            </div>
            {% endfor %}
        </div>

        <h2>Snacks</h2>
        <div class="item-container" id="snacks">
            {% for item in items.snacks %}
            <div class="item" id="snack-{{ loop.index0 }}">
                <img src="{{ item.icon }}" alt="{{ item.name }}" style="width: 50px; cursor: pointer;" onclick="addItem('snacks', {{ loop.index0 }})">
                <span>{{ item.name }}</span>
                <button class="remove" onclick="removeItem('snacks', {{ loop.index0 }})">Remover</button>
                <span class="quantity" id="quantity-snacks-{{ loop.index0 }}">0</span>
                <span class="total" id="total-snacks-{{ loop.index0 }}">0</span>
            </div>
            {% endfor %}
        </div>

        <h2>Resumo de Custos</h2>
        <div id="summary">
            <p>Total Bebidas (R$): <span id="totalBeverages">0</span></p>
            <p>Total Snacks (R$): <span id="totalSnacks">0</span></p>
            <p>Custo Total (R$): <span id="totalCost">0</span></p>
        </div>

        <h5>By Nellu</h5>
        <button class="send-whatsapp" onclick="sendWhatsApp()">
            Enviar via WhatsApp
        </button>

        <button class="install-button" id="install-button" style="display: none;">
            +
        </button>
    </div>

    <script>
        // Função para adicionar item
        function addItem(category, index) {
            fetch('/update_quantity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: category,
                    item_index: index,
                    action: 'add'
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`quantity-${category}-${index}`).innerText = data.quantity;
                document.getElementById(`total-${category}-${index}`).innerText = `R$ ${data.total.toFixed(2)}`;
                updateSummaryDisplay(data.summary);
            });
        }

        // Função para remover item
        function removeItem(category, index) {
            fetch('/update_quantity', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    category: category,
                    item_index: index,
                    action: 'remove'
                })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById(`quantity-${category}-${index}`).innerText = data.quantity;
                document.getElementById(`total-${category}-${index}`).innerText = `R$ ${data.total.toFixed(2)}`;
                updateSummaryDisplay(data.summary);
            });
        }

        // Função para atualizar o resumo na interface
        function updateSummaryDisplay(summary) {
            document.getElementById('totalBeverages').innerText = `R$ ${summary.total_beverages.toFixed(2)}`;
            document.getElementById('totalSnacks').innerText = `R$ ${summary.total_snacks.toFixed(2)}`;
            document.getElementById('totalCost').innerText = `R$ ${summary.total_cost.toFixed(2)}`;
        }

        // Variáveis globais para armazenar o estado
        let apartmentNumber;
        let beverageItems;
        let snackItems;

        // Função para enviar via WhatsApp
        function sendWhatsApp() {
            apartmentNumber = document.getElementById('apartmentNumber').value.trim();

            if (!apartmentNumber) {
                alert("Por favor, insira o número do apartamento.");
                return;
            }

            // Exibe o modal de confirmação
            document.getElementById('confirmationModal').style.display = 'flex';

            // Armazena os itens de bebidas e snacks
            beverageItems = document.getElementById('beverages').getElementsByClassName('item');
            snackItems = document.getElementById('snacks').getElementsByClassName('item');
        }

        // Função para confirmar a saída
        document.getElementById('confirmExit').onclick = function() {
            sendMessage(true); // Envia a mensagem como saída
        };

        // Função para confirmar a arrumação
        document.getElementById('confirmCleaning').onclick = function() {
            sendMessage(false); // Envia a mensagem como arrumação
        };

        // Função para enviar a mensagem
        function sendMessage(isExit) {
            const status = isExit ? ' (Saída)' : ' (Arrumação)'; // Atualiza o status para incluir "Saída"

            let message = `*Uh: ${apartmentNumber}${status} - Frigobar* \\n\\n`;

            // Coleta os itens de bebidas
            for (let item of beverageItems) {
                const name = item.getElementsByTagName('span')[0].innerText;
                const quantity = item.getElementsByClassName('quantity')[0].innerText;
                if (quantity > 0) {
                    message += `*${quantity}* ${name}\\n`;
                }
            }

            // Coleta os itens de snacks
            for (let item of snackItems) {
                const name = item.getElementsByTagName('span')[0].innerText;
                const quantity = item.getElementsByClassName('quantity')[0].innerText;
                if (quantity > 0) {
                    message += `*${quantity}* ${name}\\n`;
                }
            }

            // Adiciona o custo total à mensagem
            const totalCost = document.getElementById('totalCost').innerText;
            message += `\\n*Custo Total: ${totalCost}*`;

            // Codifica a mensagem para a URL
            const encodedMessage = encodeURIComponent(message);
            const whatsappUrl = 'whatsapp://send?text=' + encodedMessage;

            // Fecha o modal
            document.getElementById('confirmationModal').style.display = 'none';

            // Abre o WhatsApp com a mensagem
            window.open(whatsappUrl, '_blank');
            
            // Reset all quantities after sending
            fetch('/reset', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Reset UI
                    const quantities = document.querySelectorAll('.quantity');
                    const totals = document.querySelectorAll('.total');
                    
                    quantities.forEach(q => q.innerText = '0');
                    totals.forEach(t => t.innerText = '0');
                    
                    document.getElementById('totalBeverages').innerText = '0';
                    document.getElementById('totalSnacks').innerText = '0';
                    document.getElementById('totalCost').innerText = '0';
                }
            });
        }

        // Geração da lista de apartamentos
        const apartmentList = document.getElementById('apartment-list');
        const showButton = document.getElementById('show-apartments');

        showButton.onclick = () => {
            // Alterna a exibição da lista de apartamentos
            if (apartmentList.style.display === 'none' || apartmentList.style.display === '') {
                apartmentList.style.display = 'block'; // Mostra a lista
            } else {
                apartmentList.style.display = 'none'; // Esconde a lista
            }
        };

        // Gera os apartamentos
        {% for apartment in apartments %}
            const apartmentDiv = document.createElement('div');
            apartmentDiv.classList.add('apartment');
            apartmentDiv.textContent = '{{ apartment }}';
            apartmentDiv.onclick = () => {
                document.getElementById('apartmentNumber').value = '{{ apartment }}'; // Preenche o número do apartamento
                apartmentList.style.display = 'none'; // Esconde a lista após a seleção
            };
            apartmentList.appendChild(apartmentDiv);
        {% endfor %}

        // Lógica para o botão de instalação do aplicativo
        let deferredPrompt;
        const installButton = document.getElementById('install-button');

        window.addEventListener('beforeinstallprompt', (event) => {
            event.preventDefault();
            deferredPrompt = event;
            installButton.style.display = 'block'; // Mostra o botão de instalação
        });

        installButton.addEventListener('click', () => {
            installButton.style.display = 'none'; // Esconde o botão após o clique
            deferredPrompt.prompt(); // Mostra o prompt de instalação
            deferredPrompt.userChoice.then((choiceResult) => {
                if (choiceResult.outcome === 'accepted') {
                    console.log('Usuário aceitou a instalação da aplicação');
                } else {
                    console.log('Usuário recusou a instalação da aplicação');
                }
                deferredPrompt = null; // Limpa a variável
            });
        });
    </script>
</body>
</html>''')

    app.run(debug=True, host='0.0.0.0', port=5000)
