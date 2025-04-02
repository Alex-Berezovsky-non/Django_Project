def menu_data(request):
    return {
        'user': request.user,
        'is_staff': request.user.is_staff,
    }