import datetime

class ValidationError(Exception):
    pass

class TaskForm:
    def __init__(self, data=None):
        self.data = data or {}
        self.errors = {}
        self.cleaned_data = {}

    def is_valid(self):
        title = self.data.get("title")
        due_date = self.data.get("due_date")

        if not title:
            self.errors["title"] = "Title is required"
        else:
            self.cleaned_data["title"] = title

        if not due_date:
            self.errors["due_date"] = "Due date is required"
        else:
            if due_date < datetime.date.today():
                self.errors["due_date"] = "Дата не може бути в минулому."
            else:
                self.cleaned_data["due_date"] = due_date

        return not self.errors
