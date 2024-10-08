import os
import requests
import datetime
import pytz

# Obtiene el token de Slack desde los secretos de GitHub
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
CHANNEL_ID = 'S063TADEC77'  # ID del canal de Slack

# Lista de usuarios con sus IDs de Slack y horarios de lunes a jueves
USUARIOS_LUN_JUE = [
    {"id": "U04681B1JRG", "nombre": "Zaira", "inicio": "09:00", "fin": "10:17"},
    {"id": "U0463NZ1LTU", "nombre": "Nancy", "inicio": "10:17", "fin": "11:34"},
    {"id": "U07FFFQRG4D", "nombre": "Andres", "inicio": "11:34", "fin": "12:51"},
    {"id": "U078YFDTA5A", "nombre": "Julio", "inicio": "12:51", "fin": "14:08"},
    {"id": "U07QKC7TNLE", "nombre": "Andrea", "inicio": "14:08", "fin": "15:25"},
    {"id": "U054S41LQ8Y", "nombre": "Lucy", "inicio": "15:25", "fin": "16:42"},
    {"id": "U0463LXQHD0", "nombre": "Armando", "inicio": "16:42", "fin": "18:00"}
]

# Lista de usuarios con sus IDs de Slack y horarios del viernes
USUARIOS_VIE = [
    {"id": "U04681B1JRG", "nombre": "Zaira", "inicio": "09:00", "fin": "10:17"},
    {"id": "U0463NZ1LTU", "nombre": "Nancy", "inicio": "10:17", "fin": "11:34"},
    {"id": "U078YFDTA5A", "nombre": "Julio", "inicio": "11:34", "fin": "12:51"},
    {"id": "U054S41LQ8Y", "nombre": "Lucy", "inicio": "12:51", "fin": "14:08"},
    {"id": "U07QKC7TNLE", "nombre": "Andrea", "inicio": "14:08", "fin": "15:25"},
    {"id": "U07FFFQRG4D", "nombre": "Andres", "inicio": "15:25", "fin": "16:42"},
    {"id": "U0463LXQHD0", "nombre": "Armando", "inicio": "16:42", "fin": "18:00"}
]

# Función para agregar usuario a un canal
def agregar_usuario(user_id):
    url = "https://slack.com/api/conversations.invite"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    data = {"channel": CHANNEL_ID, "users": user_id}
    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    if not result.get("ok"):
        print(f"Error al agregar {user_id} al canal: {result.get('error')}")
    else:
        print(f"Usuario {user_id} agregado al canal.")
    return result

# Función para remover usuario de un canal
def remover_usuario(user_id):
    url = "https://slack.com/api/conversations.kick"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    data = {"channel": CHANNEL_ID, "user": user_id}
    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    if not result.get("ok"):
        print(f"Error al remover {user_id} del canal: {result.get('error')}")
    else:
        print(f"Usuario {user_id} removido del canal.")
    return result

# Obtener la hora actual en la zona horaria de Ciudad de México
def hora_actual():
    tz = pytz.timezone('America/Mexico_City')
    return datetime.datetime.now(tz).strftime("%H:%M")

# Obtener el día actual
def dia_actual():
    tz = pytz.timezone('America/Mexico_City')
    return datetime.datetime.now(tz).strftime("%A")

# Ejecutar según el turno actual
def ejecutar_turnos():
    hora = hora_actual()
    dia = dia_actual()
    
    # Verifica si es viernes o de lunes a jueves
    if dia in ["Monday", "Tuesday", "Wednesday", "Thursday"]:
        usuarios = USUARIOS_LUN_JUE
    elif dia == "Friday":
        usuarios = USUARIOS_VIE
    else:
        print(f"No hay turnos asignados para {dia}.")
        return
    
    # Ejecutar los turnos según el día y hora
    for usuario in usuarios:
        if usuario['inicio'] <= hora < usuario['fin']:
            print(f"Es el turno de {usuario['nombre']}, agregando al canal.")
            agregar_usuario(usuario['id'])
        else:
            print(f"Removiendo a {usuario['nombre']} del canal.")
            remover_usuario(usuario['id'])

# Llamar la función principal
ejecutar_turnos()
