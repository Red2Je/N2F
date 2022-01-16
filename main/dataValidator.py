def validate_file_type(file):
    import os 
    from django.core.exceptions import ValidationError
    ext = os.path.split(file.name)[1] #extension, [0] returns path+filename
    valid_extensions = ['.pdf','.jpg','.png','.jpeg'] # append every types you want to add to this list
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'unsupported file extension for file {file.name}')
