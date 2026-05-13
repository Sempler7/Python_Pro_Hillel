import datetime

class ValidationError(Exception):
    pass

class TaskSerializer:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}
        self.validated_data = {}

    def is_valid(self):
        title = self.data.get("title")
        due_date = self.data.get("due_date")

        if not title:
            self.errors["title"] = "Title is required"
        else:
            self.validated_data["title"] = title

        self.validated_data["description"] = self.data.get("description", "")

        if not due_date:
            self.errors["due_date"] = "Due date is required"
        else:
            if due_date < datetime.date.today():
                self.errors["due_date"] = "Дата не може бути в минулому."
            else:
                self.validated_data["due_date"] = due_date

        return not self.errors


class UserSerializer:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}
        self.validated_data = {}

    def is_valid(self):
        username = self.data.get("username")
        email = self.data.get("email")

        if not username:
            self.errors["username"] = "Username is required"
        else:
            self.validated_data["username"] = username

        if not email or "@" not in email:
            self.errors["email"] = "Valid email is required"
        else:
            self.validated_data["email"] = email

        return not self.errors


class TaskWithUserSerializer(TaskSerializer):
    def __init__(self, data=None):
        super().__init__(data)
        self.user_data = data.get("user", {})
        self.user_serializer = UserSerializer(self.user_data)

    def is_valid(self):
        parent_valid = super().is_valid()
        user_valid = self.user_serializer.is_valid()

        if not user_valid:
            self.errors["user"] = self.user_serializer.errors

        return parent_valid and user_valid
