import os
import requests
import datetime
import pytz

# Obtiene el token de Slack desde los secretos de GitHub
SLACK_TOKEN = os.getenv('SLACK_TOKEN')
USERGROUP_ID = 'S063TADEC77'  # ID del grupo de usuarios
CANAL_NOTIFICACION_ID = 'C05NQ68UVJR'  # ID del canal de notificación

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

# Función para actualizar los miembros de un grupo de usuarios
def actualizar_miembros_grupo(miembros):
    url = "https://slack.com/api/usergroups.users.update"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}"}
    data = {"usergroup": USERGROUP_ID, "users": ",".join(miembros)}
    response = requests.post(url, headers=headers, data=data)
    result = response.json()

    if not result.get("ok"):
        print(f"Error al actualizar el grupo de usuarios: {result.get('error')}")
    else:
        print(f"Grupo de usuarios actualizado con éxito.")
    return result

# Función para enviar notificación al canal
def enviar_notificacion(nombre, user_id):
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {SLACK_TOKEN}", "Content-Type": "application/json"}
    mensaje = f"Es tu hora de cubrir el chat de atencion a cliente <@{user_id}> recuerda dar lo mejor de ti"
    data = {
        "channel": CANAL_NOTIFICACION_ID,
        "text": mensaje
    }
    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if not result.get("ok"):
        print(f"Error al enviar notificación al canal: {result.get('error')}")
    else:
        print(f"Notificación enviada al canal para {nombre}.")
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
    
    # Filtrar los usuarios que deben estar en el grupo según la hora
    usuarios_en_turno = [usuario for usuario in usuarios if usuario['inicio'] <= hora < usuario['fin']]

    if usuarios_en_turno:
        for usuario in usuarios_en_turno:
            print(f"Es el turno de {usuario['nombre']}, actualizando grupo y enviando notificación.")
            actualizar_miembros_grupo([usuario['id']])
            enviar_notificacion(usuario['nombre'], usuario['id'])
    else:
        print(f"No hay usuarios en turno en este momento.")

# Llamar la función principal
ejecutar_turnos()
