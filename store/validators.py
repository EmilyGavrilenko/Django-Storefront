from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_mb = 5

    if file.size > max_size_mb * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 5MB")