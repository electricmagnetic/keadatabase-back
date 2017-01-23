from django.core.management import BaseCommand

from birds.models import Bird
from bands.models import Band, BandCombo

class Command(BaseCommand):
    help = "Allows the import of information exported from the primary Access-based database."

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING("Database import"))

        birds = Bird.objects.count()
        bands = Band.objects.count()
        band_combos = BandCombo.objects.count()

        self.stdout.write(self.style.MIGRATE_LABEL("  Current status:"))
        self.stdout.write("    Birds: %d" % birds)
        self.stdout.write("    Bands: %d" % bands)
        self.stdout.write("    Band Combos: %d" % band_combos)

        self.stdout.write(self.style.SUCCESS("Import successful!"))
