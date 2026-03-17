import pytest
from apps.employees.tests.factories import EmployeeFactory


LIST_URL = '/api/employees/'


def DETAIL_URL(pk):
    return f'/api/employees/{pk}/'

''' Note: GERENTE has exactly the same permissions as ADMIN,
    so there are no specific tests for GERENTE.
    If in the future we want to differentiate permissions, we can easily add tests for GERENTE.
'''

@pytest.mark.django_db
class TestEmployeeViewsAuthentication:

    def test_without_token_returns_401(self, api_client):
        assert api_client.get(LIST_URL).status_code == 401


@pytest.mark.django_db
class TestEmployeeViewsPermissions:

    def test_admin_can_list(self, admin_client):
        response = admin_client.get(LIST_URL)
        assert response.status_code == 200

    def test_admin_can_create(self, admin_client):
        payload = {
            'name':      'Employee Test',
            'position':  'Technician',
            'modality':  'CLT',
            'start_date': '2024-01-01',
        }
        response = admin_client.post(LIST_URL, payload)
        assert response.status_code == 201

    def test_admin_can_edit(self, admin_client, db):
        employee = EmployeeFactory()
        response = admin_client.patch(DETAIL_URL(employee.pk), {'name': 'Edited'})
        assert response.status_code == 200

    def test_admin_soft_delete(self, admin_client, db):
        from apps.employees.models import Employee
        employee = EmployeeFactory()
        employee_id = employee.pk
        response = admin_client.delete(DETAIL_URL(employee_id))
        assert response.status_code == 204
        assert not Employee.objects.filter(pk=employee_id).exists()
        assert Employee.dm_objects.filter(pk=employee_id).exists()

    def test_financeiro_can_list(self, financeiro_client):
        response = financeiro_client.get(LIST_URL)
        assert response.status_code == 200

    def test_financeiro_cannot_create(self, financeiro_client):
        payload = {'name': 'New Employee', 'start_date': '2024-01-01', 'modality': 'CLT'}
        response = financeiro_client.post(LIST_URL, payload)
        assert response.status_code == 403

    def test_financeiro_cannot_edit(self, financeiro_client, db):
        employee = EmployeeFactory()
        response = financeiro_client.patch(DETAIL_URL(employee.pk), {'name': 'Edited'})
        assert response.status_code == 403

    def test_financeiro_cannot_delete(self, financeiro_client, db):
        employee = EmployeeFactory()
        response = financeiro_client.delete(DETAIL_URL(employee.pk))
        assert response.status_code == 403
