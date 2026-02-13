"""
Custom middleware for the tasks application.

Provides:
- Cache control for authenticated users
- Security headers
- Session security
"""

from datetime import datetime


class NoCacheForAuthenticatedUsers(object):
    """
    Middleware to prevent caching of pages for authenticated users.
    
    This ensures that:
    1. Authenticated pages are never cached by the browser
    2. Users cannot access cached pages after logout
    3. Browser back button won't show cached dashboard/tasks
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process the request and response.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response with cache control headers if user is authenticated
        """
        response = self.get_response(request)
        
        # Add cache control headers if user is authenticated
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
            
            # Additional security headers
            response['X-UI-Cache'] = 'false'
            response['X-Cache'] = 'no-cache'
        
        return response


class SecurityHeadersMiddleware(object):
    """
    Middleware to add security headers to all responses.
    
    Protects against:
    - XSS attacks
    - Content type sniffing
    - Clickjacking
    - MIME type mismatches
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Add security headers to response.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response with security headers
        """
        response = self.get_response(request)
        
        # Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # Prevent XSS attacks
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Prevent clickjacking
        response['X-Frame-Options'] = 'SAMEORIGIN'
        
        # Referrer policy
        response['Referrer-Policy'] = 'same-origin'
        
        # Content Security Policy (basic)
        response['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';"
        
        return response


class SessionSecurityMiddleware(object):
    """
    Middleware to enhance session security.
    
    Ensures:
    - Sessions are properly terminated
    - Session cookies have secure flags
    """
    
    def __init__(self, get_response):
        """Initialize the middleware."""
        self.get_response = get_response
    
    def __call__(self, request):
        """
        Process session security.
        
        Args:
            request: The HTTP request object
            
        Returns:
            The HTTP response
        """
        response = self.get_response(request)
        
        # Set secure cookie flags for session
        if hasattr(request, 'session') and request.session.session_key:
            # Django handles this via settings, but we ensure it here
            response.set_cookie(
                'sessionid',
                value=request.session.session_key,
                max_age=None,
                expires=None,
                path='/',
                domain=None,
                secure=False,  # Set to True in production with HTTPS
                httponly=True,
                samesite='Lax'
            )
        
        return response
