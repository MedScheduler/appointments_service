from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

# Conectando ao MongoDB
client = AsyncIOMotorClient("mongodb://mongo:27017/")  # Conectando ao MongoDB

# Escolhendo o banco de dados
db = client["appointments_db"]  # Banco de dados para agendamento

# Escolhendo a coleção
collection = db["appointments_service"]  # Coleção para o agendamento


# Função assíncrona para inserir um agendamento
async def insert_appointment(appointment_data):
    result = await collection.insert_one(appointment_data)
    return result

# Função assíncrona para buscar todos os agendamentos
async def get_appointments():
    appointments_cursor = collection.find()
    appointments = await appointments_cursor.to_list(length=100)
    return appointments

# Função assíncrona para buscar agendamento pelo ID
async def get_appointment_by_id(appointment_id):
    appointment = await collection.find_one({"_id": ObjectId(appointment_id)})
    return appointment

# Função assíncrona para buscar agendamentos pelo ID do usuário
async def get_appointment_by_user_id(user_id):
    appointments_cursor = collection.find({"user_id": user_id})
    appointments = await appointments_cursor.to_list(length=100)
    return appointments

# Função assíncrona para buscar agendamentos pelo ID do médico
async def get_appointment_by_doctor_id(doctor_id):
    appointments_cursor = collection.find({"doctor_id": doctor_id})
    appointments = await appointments_cursor.to_list(length=100)
    return appointments

# Função assíncrona para deletar um agendamento
async def delete_appointment(appointment_id):
    result = await collection.delete_one({"_id": ObjectId(appointment_id)})
    return result

# Função assíncrona para atualizar o agendamento no MongoDB
async def update_appointment_in_db(appointment_id: str, appointment_data: dict):
    result = await collection.update_one(
        {"_id": ObjectId(appointment_id)},
        {"$set": appointment_data}
    )
    return result
