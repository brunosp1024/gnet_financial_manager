import re
from rest_framework.exceptions import ValidationError


def validate_cpf(value: str) -> None:
    """
    Valida um CPF sem máscara.
    Aceita `None` ou string vazia (não valida nesses casos).
    Levanta `rest_framework.exceptions.ValidationError` se inválido.
    """
    if value is None:
        return

    cpf = str(value).strip()
    if cpf == "":
        return
    
    cpf = cpf.replace(".", "").replace("-", "")

    if not cpf.isdigit():
        raise ValidationError('CPF deve conter apenas dígitos.')

    if len(cpf) != 11:
        raise ValidationError('CPF deve ter 11 dígitos.')

    if cpf == cpf[0] * 11:
        raise ValidationError('CPF inválido.')

    for digit in (10, 11):
        total_sum = sum(int(cpf[j]) * (digit - j) for j in range(digit - 1))
        r = 11 - (total_sum % 11)
        if r >= 10:
            r = 0
        if r != int(cpf[digit - 1]):
            raise ValidationError('CPF inválido.')

    return

def validate_phone(value: str) -> None:
    if not value:
        return

    phone = re.sub(r'[\s\-\(\)\+]', '', value)

    if not phone.isdigit():
        raise ValidationError('Telefone deve conter apenas dígitos.')

    if len(phone) not in (10, 11):
        raise ValidationError('Telefone deve ter 10 ou 11 dígitos (com DDD).')
