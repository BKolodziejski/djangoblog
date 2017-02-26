def select_theme(request):
    return {'theme_name': request.session.get('preferred_theme', 'default.css')}
