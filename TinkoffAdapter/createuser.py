from django.contrib.auth import get_user_model
# SOURCE: https://stackoverflow.com/questions/18503770/how-to-create-user-from-django-shell
# python manage.py shell < TinkoffAdapter/createuser.py


UserModel = get_user_model()

if not UserModel.objects.filter(username='javabot3').exists():
    user = UserModel.objects.create_user('javabot3', password='secret222')
    user.save()
