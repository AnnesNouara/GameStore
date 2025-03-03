def user_groups(request):
    if request.user.is_authenticated:
        return {'is_manager': request.user.groups.filter(name='Manager').exists()}
    return {'is_manager': False}