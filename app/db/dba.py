import subprocess
import os
from django.http import StreamingHttpResponse, HttpResponseServerError
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse

class FileDownload(APIView):
    def get(self, request):
        # Set the database name, username, and password
        db_name = os.environ.get('DB_NAME')
        db_user = os.environ.get('DB_USER')
        db_password = os.environ.get('DB_PASS')

        # Set the filename for the backup file
        backup_filename = 'realstate.sql'

        # Construct the path where you want to save the backup file
        backup_path = os.path.join('/path/to/backup', backup_filename)

        # Construct the pg_dump command to execute
        command = f'pg_dump --dbname={db_name} --username={db_user} --password={db_password} --file={backup_path}'

        # Execute the command to create the backup file
        try:
            subprocess.check_call(command, shell=True)
        except subprocess.CalledProcessError:
            return HttpResponseServerError('Failed to create database backup')

        # Open the backup file in binary mode
        backup_file = open(backup_path, 'rb')

        # Define a generator function to yield chunks of the backup file
        def file_iterator(file_obj, chunk_size=8192):
            while True:
                data = file_obj.read(chunk_size)
                if not data:
                    break
                yield data

        # response = StreamingHttpResponse(file_iterator(backup_file), content_type='application/x-sqlite3')
        # response['Content-Disposition'] = f'attachment; filename="{backup_filename}"'
        # return response

        with open('./{backup_filename}', 'rb') as f:
            response = FileResponse(f)
            response['Content-Disposition'] = 'attachment; filename="devdb.sql"'
            return response
