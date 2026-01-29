"""
Utilidades de validación para Kumbayah Calendar App.

Extraído de main.py líneas 306-320, 409-431 para reutilización.
Toda la lógica de validación centralizada para fácil mantenimiento y prueba.
"""
from config.app_config import AppConfig


def validate_client_data(first_name, last_name, phone):
    """
    Validar datos de entrada del cliente.
    
    Args:
        first_name (str): Nombre del cliente
        last_name (str): Apellido del cliente  
        phone (str): Número de teléfono del cliente
        
    Returns:
        tuple: (es_valido, mensaje_error)
        
    Extraído de líneas 306-308, 409-411, 418-421
    """
    if not first_name or not last_name:
        return False, AppConfig.LABELS['name_required']
        
    if not phone.isdigit():
        return False, AppConfig.LABELS['phone_digits']
        
    return True, None


def validate_reservation_data(amount, payment_method, reference):
    """
    Validar datos de entrada de reserva.
    
    Args:
        amount (str): Cadena de monto de pago
        payment_method (str): Método de pago
        reference (str): Referencia de pago
        
    Returns:
        tuple: (es_valido, mensaje_error)
        
    Extraído de líneas 312-320, 423-431
    """
    # Validate amount
    try:
        amount_val = float(amount)
    except (ValueError, TypeError):
        return False, AppConfig.LABELS['amount_invalid']
        
    # Validate reference for digital payment methods
    if payment_method in AppConfig.METHODS_REQUIRING_REFERENCE:
        if not validate_reference(reference):
            return False, AppConfig.LABELS['reference_length']
            
    return True, None


def validate_phone(phone):
    """
    Validar formato de número de teléfono.
    
    Args:
        phone (str): Número de teléfono a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
        
    Extraído de líneas 309, 420
    """
    return phone.isdigit() if phone else False


def validate_reference(reference):
    """
    Validar formato de referencia de pago.
    
    Args:
        reference (str): Referencia a validar
        
    Returns:
        bool: True si es válido, False en caso contrario
        
    Extraído de líneas 317-320, 428-431
    """
    return reference.isdigit() and len(reference) >= AppConfig.MIN_REFERENCE_LENGTH


def validate_amount(amount):
    """
    Validar y convertir cadena de monto a float.
    
    Args:
        amount (str): Cadena de monto a validar
        
    Returns:
        tuple: (es_valido, monto_float o None)
        
    Extraído de líneas 312-316, 423-427
    """
    try:
        amount_val = float(amount)
        return True, amount_val
    except (ValueError, TypeError):
        return False, None


def is_reference_required(payment_method):
    """
    Verificar si un método de pago requiere referencia.
    
    Args:
        payment_method (str): Método de pago
        
    Returns:
        bool: True si requiere referencia, False en caso contrario
    """
    return payment_method in AppConfig.METHODS_REQUIRING_REFERENCE