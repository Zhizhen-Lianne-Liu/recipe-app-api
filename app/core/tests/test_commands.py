"""
Test custom django management commands
"""

from unittest.mock import patch

from psycopg2 import OperationalError as Psycopg2Error  #  a possible error when we connect to database before it is ready

from django.core.management import call_command  #  allows us to call command we are testing

from django.db.utils import OperationalError  #  another possible error when we connect to database before it is ready

from django.test import SimpleTestCase  #  used to create unit test

@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """Test Commands"""

    def test_wait_for_db_ready(self, patched_check):
        """Test waiting for database if database ready"""
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):  #  make sure it is in this order since there is an outer patch which corresponds to the patch arg
        """Test waiting for database when getting operationalError"""
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])