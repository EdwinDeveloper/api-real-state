"""Test customs django management commands."""
from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg20p2Error

from django.core.management import call_command  # Allow us to \
# use a command we're testing
from django.db.utils import OperationalError  #
from django.test import SimpleTestCase  # Class we are using for \
# test our diferents case tests


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTest(SimpleTestCase):
    """Test commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database is ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    # patched_sleep is the first argument we \
    # have and patched_check comes from the main patch argument
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """Test waiting for database when getting OperationalError."""
        patched_check.side_effect = [Psycopg20p2Error] * 2 + \
            [OperationalError] * 3 + [True]
        # The instructions above raise an Operational Exception \
        # for try the connection agaign

        # The firsts two times we call the mock method we want \
        # to raise the Psycopg2Error

        # When the next three times we get the Psycopg2Error when \
        # we call the method we return True

        call_command('wait_for_db')

        print(patched_check.all_count)

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
