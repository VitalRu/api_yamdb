import csv

from django.core.management.base import BaseCommand

from reviews.models import Category, Title


PATH = 'static/data/'


class Command(BaseCommand):
    help = 'import data from genre.csv'

    def handle(self, *args, **kwargs):
        with open(f'{PATH}/titles.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)

                title = Title(
                    id=row[0],
                    name=row[1],
                    year=row[2],
                    category=Category(pk=row[3])
                )
                title.save()
            self.stdout.write(self.style.SUCCESS(
                f'Data from {file.name} imported successfully'
            ))
