import csv

from django.core.management.base import BaseCommand

from reviews.models import Comments
from users.models import User


PATH = 'static/data/'


class Command(BaseCommand):
    help = 'import data from genre.csv'

    def handle(self, *args, **kwargs):
        with open(f'{PATH}/comments.csv', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                print(row)

                review = Comments(
                    id=row[0],
                    review_id=row[1],
                    text=row[2],
                    author=User.objects.get(id=row[3]),
                    pub_date=row[4],
                )
                review.save()
            self.stdout.write(self.style.SUCCESS(
                f'Data from {file.name} imported successfully'
            ))
