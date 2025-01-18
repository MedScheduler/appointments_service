from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Appointment(BaseModel):
    user_id: str = Field(..., description="ID do usuário que agendou")
    doctor_id: str = Field(..., description="ID do médico que irá atender")
    service_id: str = Field(..., description="ID do serviço")
    date: datetime = Field(..., description="Data do agendamento (inclui data e hora)")
    status: str = Field(default="Aguardando Confirmação", description="Status do agendamento")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class UpdateAppointment(BaseModel):
    user_id: Optional[str] = Field(None, description="ID do usuário que agendou")
    doctor_id: Optional[str] = Field(None, description="ID do médico que irá atender")
    service_id: Optional[str] = Field(None, description="ID do serviço")
    date: Optional[datetime] = Field(None, description="Data do agendamento (inclui data e hora)")
    status: Optional[str] = Field(None, description="Status do agendamento")
    updated_at: datetime = Field(default_factory=datetime.utcnow)  # Sempre atualiza a data de modificação

