from rest_framework.permissions import BasePermission, SAFE_METHODS

#### >>> Создадим Свои классы Permissions

class IsAdmin(BasePermission):
    #Create, List
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        return request.user.is_authenticated and request.user.is_staff

    #Retrieve, Update, Delete
    def has_object_permission(self, request, view, obj):
        print(SAFE_METHODS)
        print(request.user)  # AnonymousUser - при запросе без Auth.
        print(request.user.is_authenticated) # False - Not Auth
        print(request.user.is_staff)  # False - Not Admin
        if request.method in SAFE_METHODS: #GET, OPTION, HEAD
            return True  # Если ок, безопасн метод, даем доступ
        return request.user.is_authenticated and request.user.is_staff   #is_staff = провер Админ ли

class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(dir(obj))
        return request.user.is_authenticated and (request.user == obj.owner or request.user.is_staff) # Провер он ли автор или зашел Админ