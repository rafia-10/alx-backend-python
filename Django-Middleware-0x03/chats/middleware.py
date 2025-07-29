import logging
from datetime import datetime
from collections import defaultdict
from django.http import HttpResponseForbidden


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    
    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        path = request.path
        
        log_message = f"{datetime.now()} - User: {user} - Path: {path}"

        # 🔥 Minimal logger setup (inside the __call__)
        logger = logging.getLogger("request_logger")
        logger.setLevel(logging.INFO)

        
        if not logger.handlers:
            file_handler = logging.FileHandler("request_logs.log")
            formatter = logging.Formatter('%(message)s')
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        # 📥 Log the message
        logger.info(log_message)

        return self.get_response(request)
    
class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = datetime.now().hour
        if 18 <= current_hour < 21:  # Allow access only between 6 PM and 9 PM
            return self.get_response(request)
        else:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("Access is restricted to 3 hours (6 PM - 9 PM).")
            
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response     
        
        # IP-based tracking dictionary
        #Format: {ip:[timestamp_of_Post_request]}
        self.message_logs = defaultdict(list)

        self.limit = 5  # Limit to 5 messages per user per hour
        self.time_frame = 60  # 60 minutes
    
    def __call__(self, request):  
        ip = self.get_client_ip(request)
        now = datetime.now()

        self.message_logs[ip] = [
            timestamp for timestamp in self.message_logs[ip] 
            if (now - timestamp) < self.time_frame 
        ]
        if len(self.message_logs[ip]) >= self.limit:
            return HttpResponseForbidden("You have exceeded the message limit. Please try again later.")
        
        self.message_logs[ip].append(now)

        return self.get_response(request)
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
class  RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the user has the required role
            if request.user.role == 'admin' or request.user.role == 'moderator':
                return self.get_response(request)
            else:
                return HttpResponseForbidden("You do not have permission to access this resource.")
        else:
            return HttpResponseForbidden("You must be logged in to access this resource.")
        
    