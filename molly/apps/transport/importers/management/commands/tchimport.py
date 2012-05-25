from django.core.management.base import BaseCommand, CommandError

from tch.importers.naptan import NaptanImporter
from tch.importers.nptg import NptgImporter

IMPORTERS = {
    'nptg': NptgImporter,
    'naptan': NaptanImporter,
}

class Command(BaseCommand):
    args = '<importer importer ...>'
    help = 'Runs the specified importers'

    def handle(self, *args, **options):
        if len(args) == 0:
            args = IMPORTERS.keys()
        
        for importer in args:
            if importer not in IMPORTERS:
                raise CommandError("Importer %s does not exist" % importer)
        
        for importer in args:
            print "Running %s..." % importer,
            IMPORTERS[importer]().do_import()
            print " DONE"
