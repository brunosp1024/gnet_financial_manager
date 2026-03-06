import pytest
from rest_framework.exceptions import ValidationError
from utils.validators import validate_cpf, validate_phone


# ========== CPF validation tests =========
def test_validate_cpf_accepts_valid_digits_only():
	assert validate_cpf("52998224725") is None


def test_validate_cpf_accepts_valid_masked():
	assert validate_cpf("529.982.247-25") is None


def test_validate_cpf_rejects_invalid_number():
	with pytest.raises(ValidationError):
		validate_cpf("111.111.111-11")


def test_validate_cpf_accepts_empty_string():
	assert validate_cpf("") is None


def test_validate_cpf_accepts_none():
	assert validate_cpf(None) is None


# ========== Phone validation tests =========
def test_validate_phone_accepts_empty_string():
	assert validate_phone("") is None


def test_validate_phone_accepts_none():
	assert validate_phone(None) is None


def test_validate_phone_accepts_10_digits_with_ddd():
	assert validate_phone("1132345678") is None


def test_validate_phone_accepts_11_digits_with_ddd():
	assert validate_phone("11912345678") is None


def test_validate_phone_accepts_masked_formats():
	assert validate_phone("(11) 91234-5678") is None


def test_validate_phone_rejects_non_digit_characters():
	with pytest.raises(ValidationError):
		validate_phone("11A91234567")


def test_validate_phone_rejects_invalid_length():
	with pytest.raises(ValidationError):
		validate_phone("119123456")
