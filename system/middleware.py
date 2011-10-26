import django.http
import django.template

class CreateSystemMiddleware(object):
  """Checks if the session has the system_being_created variable turned on, and turn it of if it's needed
  """
  def process_request(self, request):
    
    #print request.session["system_being_created"]
    #print request

    return None
