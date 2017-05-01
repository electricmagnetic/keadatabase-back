from django.core import management

from synchronise.locations import synchronise_StudyArea
from locations.models import StudyArea

class Command(management.BaseCommand):
    help = "Allows the import of tables exported from the Access database."

    def check_current_status(self):
        """ Outputs information about objects currently in database """
        self.stdout.write(self.style.MIGRATE_HEADING("Current status:"))
        self.stdout.write("StudyArea: %d" % StudyArea.objects.count())

    def do_import(self):
        """ Imports objects into database """
        self.stdout.write(self.style.MIGRATE_HEADING("\nBeginning import:"))

        synchronise_StudyArea(self, "../data/tStudyAreas.csv")

        self.stdout.write(self.style.SUCCESS("\nImport complete"))

    def handle(self, *args, **options):
        self.check_current_status()

        #confirm = input("\nReady to import? Type 'yes' to continue: ")
        confirm = 'yes' # for debugging

        if confirm == 'yes':
            self.do_import()
        else:
            self.stdout.write("\nImport cancelled!")
