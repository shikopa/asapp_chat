from django.contrib.auth.models import  User
from django.core.management.base import BaseCommand

DEFAULT_PASSWORD = 'test1234'

# Users
USERS = [
    {'username': 'george', 'first_name': 'George', 'last_name': 'Johns', 'email': 'george.johns@example.com'},
    {'username': 'john', 'first_name': 'John', 'last_name': 'Smith', 'email': 'john.smith@example.com'},
    {'username': 'jane', 'first_name': 'Jane', 'last_name': 'Reids', 'email': 'jane.reids@example.com'},
    {'username': 'jack', 'first_name': 'Jack', 'last_name': 'Jones', 'email': 'jack.jones@example.com'},
    {'username': 'andy', 'first_name': 'Andy', 'last_name': 'Diggs', 'email': 'andy.diggss@example.com'},
]


class Command(BaseCommand):
    args = ''
    help = 'Loads Initial Data For The App'

    def handle(self, *args, **options):
        # Create Admin User
        self.generate_admin_user()

        # Create Users
        self.generate_users()


    @classmethod
    def generate_admin_user(cls):
        if not User.objects.filter(username=u'admin').exists():
            User.objects.create_superuser(
                username=u'admin',
                email=u'admin@example.com',
                password=DEFAULT_PASSWORD,
                first_name=u'Admin',
                last_name=u'Administrator',
            )
            print "Created the Admin User : 'admin'"

    @classmethod
    def generate_users(cls):
        for u in USERS:
            if not User.objects.filter(username=u['username']).exists():
                User.objects.create_user(
                    username=u['username'],
                    email=u['email'],
                    password='',
                    first_name=u['first_name'],
                    last_name=u['last_name'],
                )
                print "Created the User : '{0}'".format(u['username'])
