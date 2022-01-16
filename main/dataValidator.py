def validate_file_type(file):
    import os 
    from django.core.exceptions import ValidationError
    name,ext = os.path.splitext(file.name)
    valid_extensions = ['.pdf','.jpg','.png','.jpeg'] # append every types you want to add to this list
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'unsupported file extension for file {file.name}')
