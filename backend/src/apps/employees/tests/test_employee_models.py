import pytest
from apps.employees.models import Employee
from apps.employees.tests.factories import EmployeeFactory


@pytest.mark.django_db
class TestEmployeeModel:

    def test_create_employee(self):
        e = EmployeeFactory(name='Roberto Lima', position='Técnico')
        assert e.pk is not None
        assert e.name == 'Roberto Lima'
        assert e.position == 'Técnico'
        assert e.modality == Employee.Modality.CLT  # Default value
