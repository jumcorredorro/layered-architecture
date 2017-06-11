from rolepermissions.roles import AbstractUserRole

class Administrator(AbstractUserRole):
    available_permissions = {
        'delete_album': True,
    }

class Coordinador(AbstractUserRole):
    available_permissions = {
        'add_album': True,
    }

class Consulta(AbstractUserRole):
    available_permissions = {
        'see_album': True,
    }
