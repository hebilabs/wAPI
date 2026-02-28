class User:
    def __init__(self, id, fullname, email, password, address, is_admin):
        self.id = id
        self.fullname = fullname
        self.email = email
        self.password = password
        self.address = address
        self.is_admin = is_admin