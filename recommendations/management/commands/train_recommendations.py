from django.core.management.base import BaseCommand
from recommendations.utils import train_item_similarity, train_co_occurrence

class Command(BaseCommand):
    help = 'Trains recommendation models'

    def handle(self, *args, **kwargs):
        self.stdout.write('Training item similarity...')
        train_item_similarity()
        
        self.stdout.write('Training co-occurrence...')
        train_co_occurrence()
        
        self.stdout.write(self.style.SUCCESS('Successfully trained recommendation models'))
