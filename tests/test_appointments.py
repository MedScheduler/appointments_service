import sys
import os

# Adicionando o diretório raiz ao caminho de importação
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
import pytest
from datetime import datetime
from app.models import Appointment  # Assumindo que seu modelo está no diretório app.models

# Teste básico para criação de um agendamento
def test_create_appointment():
    # Criação de uma instância de Appointment com dados fictícios
    appointment = Appointment(
        user_id="123", 
        service_id="abc", 
        date=datetime(2025, 1, 17, 14, 30)
    )
    
    # Verificando se os dados foram atribuídos corretamente
    assert appointment.user_id == "123"
    assert appointment.service_id == "abc"
    assert appointment.date == datetime(2025, 1, 17, 14, 30)
    assert appointment.status == "Aguardando Confirmação"
    assert appointment.created_at is not None
    assert appointment.updated_at is not None

# Teste de valores padrão
def test_default_values():
    # Criação de uma instância de Appointment sem fornecer valores de status, created_at, updated_at
    appointment = Appointment(
        user_id="456", 
        service_id="def", 
        date=datetime(2025, 1, 18, 15, 00)
    )
    
    # Verificando se o valor padrão de status foi atribuído corretamente
    assert appointment.status == "Aguardando Confirmação"
    assert appointment.created_at is not None
    assert appointment.updated_at is not None

# Teste de validação de dados (erro de tipo)
def test_invalid_data():
    with pytest.raises(ValueError):  # Esperamos que lance um ValueError se o tipo de dado estiver errado
        Appointment(
            user_id="123", 
            service_id="abc", 
            date="invalid_date"  # Data inválida, deve lançar um erro
        )
