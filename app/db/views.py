from django.http import HttpResponseServerError
from rest_framework.decorators import api_view
import subprocess
from django.conf import settings
from django.http import FileResponse

@api_view(['GET'])
def download_database_backup_view(request):
    try:
        response = download_database_backup(request)
        return response
    except Exception as e:
        return HttpResponseServerError(str(e))
    

def download_database_backup(request):
    db_config = settings.DATABASES['default']
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST'] or 'localhost'
    db_port = db_config['PORT'] or '5432'
    filename = f'{db_name}.sql'

    # backup_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -Fc {db_name}'
    backup_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -f {filename} {db_name}'
    # backup_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -F c -f /Users/edwingiovanni/Downloads/backup_file.dump {db_name}'
    # backup_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -f /Users/edwingiovanni/Downloads/backup_file.sql {db_name} --password="{db_password}" -v'
    # backup_command = f'pg_dump -h {db_host} -p {db_port} -U {db_user} -F c -f /path/to/backup_file.dump {db_name} --password="{db_password}"'
    if db_password:
        backup_command = f'PGPASSWORD="{db_password}" {backup_command}'

    backup_file = subprocess.Popen(
        backup_command,
        stdout=subprocess.PIPE,
        shell=True
    ).communicate()[0]

    response = FileResponse(backup_file, content_type='application/octet-stream')
    response['Content-Disposition'] = f'attachment; filename={filename}'

    return response