# myapp/middleware/auto_logout.py

from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import logout
from django.utils import timezone
import datetime

class AutoLogout(MiddlewareMixin):
    def process_request(self, request):
        if not request.user.is_authenticated:
            return  # Skip if user is not logged in

        last_activity = request.session.get('last_activity')

        if last_activity:
            last_activity = datetime.datetime.fromisoformat(last_activity)
            now = datetime.datetime.now()

            # Check if more than 5 minutes (300 seconds) passed
            if (now - last_activity).total_seconds() > 10:
                logout(request)  # Force logout
                return

        # Update the last activity time
        request.session['last_activity'] = datetime.datetime.now().isoformat()
