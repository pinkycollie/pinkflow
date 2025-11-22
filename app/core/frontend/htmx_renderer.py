"""
HTMX enhanced renderer with accessibility support.
Dynamically selects templates based on user preferences.
"""
from flask import render_template, g
from app.models import User


class HTMXRenderer:
    """Base HTMX renderer."""
    
    @staticmethod
    def render(template_name, **context):
        """
        Render a template with context.
        
        Args:
            template_name: Name of the template file
            **context: Template context variables
            
        Returns:
            Rendered HTML string
        """
        return render_template(template_name, **context)


class HTMXEnhancedRenderer(HTMXRenderer):
    """Enhanced HTMX renderer with accessibility features."""
    
    @staticmethod
    def render_with_accessibility(template_name, user_preferences=None, **context):
        """
        Render template with accessibility enhancements.
        
        Automatically selects the appropriate template variant based on
        user's visual density preference and adds accessibility context.
        
        Args:
            template_name: Base template name (without variant suffix)
            user_preferences: Optional user preferences dict
            **context: Additional template context
            
        Returns:
            Rendered HTML string
        """
        # Get user preferences
        if not user_preferences and hasattr(g, 'user_id'):
            user = User.query.get(g.user_id)
            user_preferences = user.accessibility_preferences if user else {}
        
        if not user_preferences:
            user_preferences = {}
        
        # Add accessibility context
        context.update({
            'visual_density': user_preferences.get('visual_density', 3),
            'sign_language': user_preferences.get('preferred_sign_language', 'ASL'),
            'motion_sensitive': user_preferences.get('motion_sensitivity', False),
            'high_contrast': user_preferences.get('color_contrast') == 'high',
            'reading_level': user_preferences.get('reading_level', 3)
        })
        
        # Select appropriate template variant based on visual density
        # 1: minimal, 2: low, 3: normal, 4: rich, 5: max
        template_variants = {
            1: f"{template_name}_minimal.html",
            2: f"{template_name}_low.html",
            3: f"{template_name}.html",
            4: f"{template_name}_rich.html",
            5: f"{template_name}_max.html"
        }
        
        density = context['visual_density']
        actual_template = template_variants.get(density, f"{template_name}.html")
        
        # Try to render the variant, fall back to normal template if not found
        try:
            return HTMXRenderer.render(actual_template, **context)
        except Exception:
            # Fall back to base template if variant doesn't exist
            return HTMXRenderer.render(f"{template_name}.html", **context)
    
    @staticmethod
    def render_partial(partial_name, **context):
        """
        Render a partial template (component).
        
        Partials are typically smaller reusable components that are
        loaded via HTMX swaps.
        
        Args:
            partial_name: Name of the partial template
            **context: Template context
            
        Returns:
            Rendered HTML string
        """
        return HTMXRenderer.render(f"partials/{partial_name}.html", **context)
    
    @staticmethod
    def get_htmx_headers(request):
        """
        Extract HTMX-specific headers from request.
        
        Args:
            request: Flask request object
            
        Returns:
            Dictionary of HTMX headers
        """
        return {
            'hx_request': request.headers.get('HX-Request', 'false') == 'true',
            'hx_trigger': request.headers.get('HX-Trigger'),
            'hx_trigger_name': request.headers.get('HX-Trigger-Name'),
            'hx_target': request.headers.get('HX-Target'),
            'hx_current_url': request.headers.get('HX-Current-URL'),
            'hx_prompt': request.headers.get('HX-Prompt')
        }
    
    @staticmethod
    def is_htmx_request(request):
        """
        Check if the request is an HTMX request.
        
        Args:
            request: Flask request object
            
        Returns:
            Boolean indicating if request is from HTMX
        """
        return request.headers.get('HX-Request', 'false') == 'true'
