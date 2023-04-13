from uuid import uuid4 
from django_seed import Seed

from django.core.management.base import BaseCommand, CommandError
from todo.models import Task, Category



class Command(BaseCommand):
    help = "Seed the database with some initial data"

    def add_arguments(self, parser):
        parser.add_argument("--delete", action="store_true", help="Delete all records before seeding")

    def handle(self, *args, **options):
        
        if options["delete"]:
            Task.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.NOTICE("Successfully deleted records"))
            return
        
        seeder = Seed.seeder()

        seeder.add_entity(Category, 20, {
            'uuid': lambda x: uuid4(),
            'name': lambda x: seeder.faker.word(),
        })

        seeder.add_entity(Task, 100, {
            'uuid': lambda x: uuid4(),
            'title': lambda x: seeder.faker.sentence(nb_words=4).lower()[:-1],
        })

        try:
            seeder.execute()
            self.stdout.write(self.style.SUCCESS(f"Successfully seeded the database"))
        except Exception as e:
            raise CommandError(e)

        