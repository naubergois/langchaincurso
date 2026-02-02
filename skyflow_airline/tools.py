import random
from datetime import datetime, timedelta

def search_flights(origin: str, destination: str):
    """Procura voos entre duas cidades."""
    cities = ["São Paulo", "Rio de Janeiro", "Paris", "Londres", "Nova York", "Tóquio"]
    if origin not in cities or destination not in cities:
        return f"Desculpe, não operamos voos entre {origin} e {destination} no momento."
    
    flights = [
        {"flight": "SF101", "price": random.randint(300, 1500), "time": "10:00", "duration": "12h"},
        {"flight": "SF202", "price": random.randint(400, 2000), "time": "15:30", "duration": "11h 30m"},
        {"flight": "SF303", "price": random.randint(500, 2500), "time": "22:15", "duration": "13h"},
    ]
    return f"Encontrei os seguintes voos de {origin} para {destination}:\n" + \
           "\n".join([f"- {f['flight']}: R$ {f['price']} às {f['time']} (Duração: {f['duration']})" for f in flights])

def check_flight_status(flight_number: str):
    """Verifica o status e o portão de um voo específico."""
    statuses = ["No horário", "Atrasado", "Cancelado", "Embarque Próximo"]
    gates = ["A1", "B12", "C5", "D20", "Portão não definido"]
    
    status = random.choice(statuses)
    gate = random.choice(gates)
    
    return f"Voo {flight_number}:\nStatus: {status}\nPortão: {gate}"

def create_support_ticket(complaint_type: str, details: str):
    """Registra uma reclamação ou pedido de suporte."""
    ticket_id = random.randint(10000, 99999)
    return f"Ticket de Suporte #{ticket_id} criado para: {complaint_type}.\nDetalhes: {details}\nNossa equipe entrará em contato em breve."

# Dicionário de ferramentas para facilitar o uso no LangChain
TOOLS = {
    "search_flights": search_flights,
    "check_flight_status": check_flight_status,
    "create_support_ticket": create_support_ticket
}
