import requests
from json import dumps
from fastapi import APIRouter, HTTPException, status
from app.models import Appointment, UpdateAppointment
from app.kafka.producer import send_event
from app.database import (
    insert_appointment, get_appointments, get_appointment_by_id, delete_appointment, update_appointment_in_db, get_appointment_by_user_id, get_appointment_by_doctor_id
)
from bson import ObjectId

router = APIRouter()

# Criar agendamento
@router.post("/appointments", status_code=status.HTTP_201_CREATED)
async def create_appointment(appointment: Appointment):
    appointment_data = appointment.dict()
    result = await insert_appointment(appointment_data)
    send_event(appointment_data)
    return {"id": str(result.inserted_id), "message": "Appointment created successfully"}

# Listar agendamentos
@router.get("/appointments")
async def get_appointments_route():
    appointments = await get_appointments()
    for appointment in appointments:
        appointment["_id"] = str(appointment["_id"])
    return appointments

# Buscar agendamento por ID
@router.get("/appointments/{appointment_id}")
async def get_appointment(appointment_id: str):
    appointment = await get_appointment_by_id(appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    user_ids  = [appointment["doctor_id"], appointment["user_id"]]
    query_params = {"ids": user_ids}

    response = requests.get("http://user_service:8006/user", params=query_params)
    external_data = response.json()

    doctor = {doctor['id']: doctor for doctor in external_data.get('data', [])}
    patient = {patient['id']: patient for patient in external_data.get('data', [])}

    appointment["_id"] = str(appointment["_id"])
    appointment["patient"] = patient[int(appointment.get("user_id"))]
    appointment["doctor"] = doctor[int(appointment.get("doctor_id"))]
    return appointment

# Buscar agendamentos por ID do paciente
@router.get("/appointments/patient/{user_id}")
async def get_appointment(user_id: str):
    appointments = await get_appointment_by_user_id(user_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")

    unique_user_ids = list(set(
        appointment["doctor_id"] for appointment in appointments
    ).union(
        appointment["user_id"] for appointment in appointments
    ))
    query_params = {"ids": unique_user_ids}

    review_params = ",".join(list(set(
        str(appointment["_id"]) for appointment in appointments
    )))

    review_response = requests.get("".join("http://review_service:8003/api/v1/reviews/apointment-ids/"+review_params))
    external_review_data = review_response.json();

    response = requests.get("http://user_service:8006/user", params=query_params)
    external_data = response.json()

    doctors = {doctor['id']: doctor for doctor in external_data.get('data', [])}
    patients = {patient['id']: patient for patient in external_data.get('data', [])}
    reviews = {}
    appointment_id=''
    review = {}
    for review in external_review_data:
        appointment_id = review['appointment_id']
    if appointment_id not in reviews:
        reviews[appointment_id] = review


    for appointment in appointments:
        appointment["_id"] = str(appointment["_id"])
        appointment["patient"] = patients[int(appointment.get("user_id"))]
        appointment["doctor"] = doctors[int(appointment.get("doctor_id"))]
        appointment["review"] = reviews.get(appointment["_id"])

    return appointments

# Buscar agendamentos por ID do médico
@router.get("/appointments/doctor/{doctor_id}")
async def get_appointment(doctor_id: str):
    appointments = await get_appointment_by_doctor_id(doctor_id)
    if not appointments:
        raise HTTPException(status_code=404, detail="Appointment not found")

    unique_user_ids = list(set(
        appointment["doctor_id"] for appointment in appointments
    ).union(
        appointment["user_id"] for appointment in appointments
    ))
    query_params = {"ids": unique_user_ids}

    response = requests.get("http://user_service:8006/user", params=query_params)
    external_data = response.json()
    doctors = {doctor['id']: doctor for doctor in external_data.get('data', [])}
    patients = {patient['id']: patient for patient in external_data.get('data', [])}

    for appointment in appointments:
        appointment["_id"] = str(appointment["_id"])
        appointment["patient"] = patients[int(appointment.get("user_id"))]
        appointment["doctor"] = doctors[int(appointment.get("doctor_id"))]

    return appointments

# Deletar agendamento
@router.delete("/appointments/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment_route(appointment_id: str):
    result = await delete_appointment(appointment_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment deleted successfully"}

# Atualizar agendamento
@router.put("/appointments/{appointment_id}", status_code=status.HTTP_200_OK)
async def update_appointment(appointment_id: str, appointment: UpdateAppointment):
    appointment_data = appointment.dict(exclude_unset=True)
    result = await update_appointment_in_db(appointment_id, appointment_data)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return {"message": "Appointment updated successfully"}
