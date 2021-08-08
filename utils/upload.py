
def save_uploaded_file(path:str, file):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)