"""
Django command to wait for the database to be available.
"""
import subprocess
import time

from django.conf import settings
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2OpError


class Command(BaseCommand):
    """Django command to wait for database."""

    help = "Wait for database to be ready."

    def handle(self, *args, **options):
        """Entrypoint for command."""
        self.stdout.write("Waiting for database...")

        db_user=settings.DATABASES['default']['USER']
        db_pass=settings.DATABASES['default']['PASSWORD']
        db_host=settings.DATABASES['default']['HOST']
        db_name=settings.DATABASES['default']['NAME']

        db_up = False
        while db_up is False:
            try:
                # Use the pg_isready command line tool provided by postgres to check if the
                # database is accepting connection.
                #
                # The username and password is provided in the connection string, but the
                # tool will not confirm if the login was successful. However, this can be
                # checked in the postgres logs.
                pg_isready = subprocess.run(
                    ["pg_isready", "-d", (f"postgresql://{db_user}:{db_pass}@{db_host}/{db_name}")],
                    capture_output=True,
                    )
                assert "accepting connections" in str(pg_isready.stdout)

                # This is another check using the built in django check, but it is not as robust
                # as the one above. However, the one above is postgres specific.
                self.check(databases=['default'])
                db_up = True

            except (AssertionError, Psycopg2OpError, OperationalError):
                self.stdout.write("Database unavailable, waiting 1 second...")
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS("Database ready!"))