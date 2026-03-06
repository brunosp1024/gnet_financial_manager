from rest_framework.permissions import BasePermission


GROUPS_PERMISSIONS = {
    'ADMIN': {
        'users':     ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'me'],
        'employees': ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        'customers': ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        'finance':   ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'daily_report', 'dashboard'],
    },
    'GERENTE': {
        'users':        ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'me'],
        'employees':    ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        'customers':    ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        'finance':      ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'daily_report', 'dashboard'],
    },
    'FINANCEIRO': {
        'users':        ['list', 'retrieve', 'me'],
        'employees':    ['list', 'retrieve'],
        'customers':    ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy'],
        'finance':      ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy', 'daily_report', 'dashboard'],
    },
}


class GroupPermission(BasePermission):
    """
    Lê `resource` da view para identificar o módulo,
    e `action` do ViewSet para checar se o grupo tem permissão.

    Uso na view:
        resource = 'transactions'
        permission_classes = [GroupPermission]
    """

    def _get_resource(self, view):
        resource = getattr(view, "permission_resource", None)
        if resource:
            return resource

        model = None
        queryset = getattr(view, "queryset", None)
        if queryset is not None:
            model = getattr(queryset, "model", None)

        if model is None and hasattr(view, "get_queryset"):
            try:
                model = view.get_queryset().model
            except Exception:
                model = None

        return model._meta.app_label if model else None

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        resource = self._get_resource(view)
        action   = getattr(view, 'action', None)

        if not resource or not action:
            return False

        user_groups = request.user.groups.values_list('name', flat=True)

        return any(
            action in GROUPS_PERMISSIONS.get(group, {}).get(resource, [])
            for group in user_groups
        )
