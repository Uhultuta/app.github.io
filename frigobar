import http.server
import socketserver
import json
import os
from urllib.parse import parse_qs

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

class FrigobarHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            
            # Generate HTML content
            html_content = self.generate_html()
            self.wfile.write(html_content.encode('utf-8'))
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path == '/update_quantity':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            
            category = data.get('category')
            item_index = data.get('item_index')
            action = data.get('action')
            
            response_data = {}
            if category in ITEMS and 0 <= item_index < len(ITEMS[category]):
                if action == 'add':
                    ITEMS[category][item_index]['quantity'] += 1
                elif action == 'remove' and ITEMS[category][item_index]['quantity'] > 0:
                    ITEMS[category][item_index]['quantity'] -= 1
                
                response_data = {
                    'quantity': ITEMS[category][item_index]['quantity'],
                    'total': ITEMS[category][item_index]['quantity'] * ITEMS[category][item_index]['price'],
                    'summary': self.calculate_summary()
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        
        elif self.path == '/reset':
            for category in ITEMS:
                for item in ITEMS[category]:
                    item['quantity'] = 0
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def calculate_summary(self):
        total_beverages = sum(item['quantity'] * item['price'] for item in ITEMS['beverages'])
        total_snacks = sum(item['quantity'] * item['price'] for item in ITEMS['snacks'])
        total_cost = total_beverages + total_snacks
        
        return {
            'total_beverages': total_beverages,
            'total_snacks': total_snacks,
            'total_cost': total_cost
        }
    
    def generate_html(self):
        beverages_html = ""
        for i, item in enumerate(ITEMS['beverages']):
            beverages_html += f'''
            <div class="item" id="beverage-{i}">
                <img src="{item['icon']}" alt="{item['name']}" style="width: 50px; cursor: pointer;" onclick="addItem('beverages', {i})">
                <span>{item['name']}</span>
                <button class="remove" onclick="removeItem('beverages', {i})">Remover</button>
                <span class="quantity" id="quantity-beverages-{i}">0</span>
                <span class="total" id="total-beverages-{i}">0</span>
            </div>
            '''
        
        snacks_html = ""
        for i, item in enumerate(ITEMS['snacks']):
            snacks_html += f'''
            <div class="item" id="snack-{i}">
                <img src="{item['icon']}" alt="{item['name']}" style="width: 50px; cursor: pointer;" onclick="addItem('snacks', {i})">
                <span>{item['name']}</span>
                <button class="remove" onclick="removeItem('snacks', {i})">Remover</button>
                <span class="quantity" id="quantity-snacks-{i}">0</span>
                <span class="total" id="total-snacks-{i}">0</span>
            </div>
            '''
        
        apartments_html = ""
        for apartment in APARTMENTS:
            apartments_html += f'''
            <div class="apartment" onclick="selectApartment('{apartment}')">
                {apartment}
            </div>
            '''
        
        return f'''
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Frigobar</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 20px;
            color: #333;
        }}

        .container {{
            max-width: 600px;
            margin: auto;
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
            position: relative;
        }}

        h1, h2 {{
            color: #2c3e50;
            text-align: center;
        }}

        .apartment-list {{
            display: none;
            margin-top: 20px;
        }}

        .apartment {{
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
        }}

        .apartment:hover {{
            background: #0056b3;
        }}

        .item-container {{
            margin-bottom: 20px;
        }}

        .item {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 15px;
            border: 1px solid #ddd;
            border-radius: 5px;
            margin-bottom: 10px;
            background-color: #ecf0f1;
            transition: background-color 0.3s;
        }}

        .item:hover {{
            background-color: #dfe6e9;
        }}

        .item button {{
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 5px;
            padding: 8px 12px;
            cursor: pointer;
            transition: background-color 0.3s;
        }}

        .item button.remove {{
            background-color: #e74c3c;
        }}

        .item button:hover {{
            background-color: #2980b9;
        }}

        .item button.remove:hover {{
            background-color: #c0392b;
        }}

        .quantity, .total {{
            margin-left: 10px;
            font-weight: bold;
        }}

        #summary {{
            margin-top: 20px;
            font-size: 1.2em;
            text-align: center;
        }}

        .input-apartment {{
            margin-bottom: 20px;
            text-align: center;
        }}

        .input-apartment input {{
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            width: calc(100% - 22px);
            max-width: 300px;
        }}

        button.send-whatsapp {{
            background-color: #25D366;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            display: block;
            margin: 20px auto;
            transition: background-color 0.3s;
        }}

        button.send-whatsapp:hover {{
            background-color: #1da851;
        }}

        h5 {{
            text-align: center;
            font-size: 0.9em;
            color: #7f8c8d;
        }}

        #show-apartments {{
            background-color: blue;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
            border-radius: 5px;
            display: block;
            margin: 20px auto;
        }}

        #confirmationModal {{
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            display: none;
            justify-content: center;
            align-items: center;
        }}

        .modal-content {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            text-align: center;
        }}
    </style>
</head>
<body>

    <div id="confirmationModal">
        <div class="modal-content">
            <p>Foi saída ou arrumação?</p>
            <button id="confirmExit">Saída</button>
            <button id="confirmCleaning">Arrumação</button>
        </div>
    </div>

    <div class="container">
        <h1>Frigobar</h1>

        <div class="input-apartment">
            <label for="apartmentNumber"><strong>Número do Apartamento:</strong></label>
            <input type="text" id="apartmentNumber" placeholder="Digite o número do apartamento" />
        </div>

        <button id="show-apartments">Selecionar Apartamentos</button>

        <div class="apartment-list" id="apartment-list">
            {apartments_html}
        </div>

        <h2>Bebidas</h2>
        <div class="item-container" id="beverages">
            {beverages_html}
        </div>

        <h2>Snacks</h2>
        <div class="item-container" id="snacks">
            {snacks_html}
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
    </div>

    <script>
        function addItem(category, index) {{
            fetch('/update_quantity', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    category: category,
                    item_index: index,
                    action: 'add'
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById(`quantity-${{category}}-${{index}}`).innerText = data.quantity;
                document.getElementById(`total-${{category}}-${{index}}`).innerText = `R$ ${{data.total.toFixed(2)}}`;
                updateSummaryDisplay(data.summary);
            }});
        }}

        function removeItem(category, index) {{
            fetch('/update_quantity', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }},
                body: JSON.stringify({{
                    category: category,
                    item_index: index,
                    action: 'remove'
                }})
            }})
            .then(response => response.json())
            .then(data => {{
                document.getElementById(`quantity-${{category}}-${{index}}`).innerText = data.quantity;
                document.getElementById(`total-${{category}}-${{index}}`).innerText = `R$ ${{data.total.toFixed(2)}}`;
                updateSummaryDisplay(data.summary);
            }});
        }}

        function updateSummaryDisplay(summary) {{
            document.getElementById('totalBeverages').innerText = `R$ ${{summary.total_beverages.toFixed(2)}}`;
            document.getElementById('totalSnacks').innerText = `R$ ${{summary.total_snacks.toFixed(2)}}`;
            document.getElementById('totalCost').innerText = `R$ ${{summary.total_cost.toFixed(2)}}`;
        }}

        function selectApartment(apartment) {{
            document.getElementById('apartmentNumber').value = apartment;
            document.getElementById('apartment-list').style.display = 'none';
        }}

        function sendWhatsApp() {{
            const apartmentNumber = document.getElementById('apartmentNumber').value.trim();

            if (!apartmentNumber) {{
                alert("Por favor, insira o número do apartamento.");
                return;
            }}

            document.getElementById('confirmationModal').style.display = 'flex';
        }}

        document.getElementById('confirmExit').onclick = function() {{
            sendMessage(true);
        }};

        document.getElementById('confirmCleaning').onclick = function() {{
            sendMessage(false);
        }};

        function sendMessage(isExit) {{
            const status = isExit ? ' (Saída)' : ' (Arrumação)';
            const apartmentNumber = document.getElementById('apartmentNumber').value.trim();

            let message = `*Uh: ${{apartmentNumber}}${{status}} - Frigobar* \\n\\n`;

            // Collect beverages
            const beverageItems = document.getElementById('beverages').getElementsByClassName('item');
            for (let item of beverageItems) {{
                const name = item.getElementsByTagName('span')[0].innerText;
                const quantity = item.getElementsByClassName('quantity')[0].innerText;
                if (quantity > 0) {{
                    message += `*${{quantity}}* ${{name}}\\n`;
                }}
            }}

            // Collect snacks
            const snackItems = document.getElementById('snacks').getElementsByClassName('item');
            for (let item of snackItems) {{
                const name = item.getElementsByTagName('span')[0].innerText;
                const quantity = item.getElementsByClassName('quantity')[0].innerText;
                if (quantity > 0) {{
                    message += `*${{quantity}}* ${{name}}\\n`;
                }}
            }}

            const totalCost = document.getElementById('totalCost').innerText;
            message += `\\n*Custo Total: ${{totalCost}}*`;

            const encodedMessage = encodeURIComponent(message);
            const whatsappUrl = 'whatsapp://send?text=' + encodedMessage;

            document.getElementById('confirmationModal').style.display = 'none';

            // Reset after sending
            fetch('/reset', {{
                method: 'POST',
                headers: {{
                    'Content-Type': 'application/json',
                }}
            }}).then(() => {{
                const quantities = document.querySelectorAll('.quantity');
                const totals = document.querySelectorAll('.total');
                
                quantities.forEach(q => q.innerText = '0');
                totals.forEach(t => t.innerText = '0');
                
                document.getElementById('totalBeverages').innerText = '0';
                document.getElementById('totalSnacks').innerText = '0';
                document.getElementById('totalCost').innerText = '0';
                
                window.open(whatsappUrl, '_blank');
            }});
        }}

        document.getElementById('show-apartments').onclick = () => {{
            const apartmentList = document.getElementById('apartment-list');
            apartmentList.style.display = apartmentList.style.display === 'none' ? 'block' : 'none';
        }};
    </script>
</body>
</html>
'''

def main():
    PORT = 8000
    with socketserver.TCPServer(("", PORT), FrigobarHandler) as httpd:
        print(f"Servidor Frigobar rodando na porta {PORT}")
        print(f"Acesse: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    main()
