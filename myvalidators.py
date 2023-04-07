from wtforms.validators import ValidationError

class FloatRange:
    def __init__(self, min=None, max=None, message=None):
        self.min = min
        self.max = max
        self.message = message

    def __call__(self, form, field):
        try:
            value = float(field.data)
        except ValueError:
            raise ValidationError('Invalid float number')

        if self.min is not None and value < self.min:
            message = self.message or f'Number must be greater than or equal to {self.min}'
            raise ValidationError(message)

        if self.max is not None and value > self.max:
            message = self.message or f'Number must be less than or equal to {self.max}'
            raise ValidationError(message)
