import os
import time
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin

class CleanupTemporaryFilesMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if hasattr(request, '_delete_temp_file'):
            file_path = request._delete_temp_file
            if os.path.exists(file_path):
                # Aguarda um breve período antes de remover o arquivo
                time.sleep(5)
                os.remove(file_path)
        return response
