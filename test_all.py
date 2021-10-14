import unittest
import sql_functions as sqlf
import tests


class testtests(unittest.TestCase):

    def test_between(self):

        self.assertTrue(tests.between("Tekst", 3, 6))
        self.assertTrue(tests.between("Tekst", 5, 5))

        self.assertFalse(tests.between("Tekst", 1, 3))
        self.assertFalse(tests.between("Tekst", 6, 9))

    def test_legalchars(self):

        # brukernavn
        self.assertTrue(tests.using_legalcharacters("Tekst", "username"))
        self.assertTrue(tests.using_legalcharacters("_Tekst3_", "username"))

        self.assertFalse(tests.using_legalcharacters("_Tek#t3_", "username"))
        self.assertFalse(tests.using_legalcharacters(
            "mell mellom omrom", "username"))

        # passord (nesten lik: flere tegn)
        self.assertTrue(tests.using_legalcharacters("_Tek#t3_", "password"))

        self.assertFalse(tests.using_legalcharacters(
            "ÆÆÅ_T£$ek#t3_*", "password"))

    def test_requirements(self):

        self.assertTrue(tests.meets_requirements("Pass1.", 1, 1, 1, 1))
        self.assertTrue(tests.meets_requirements("PAss1.", 1, 2, 1, 1))

        self.assertFalse(tests.meets_requirements("Pass1", 1, 1, 1, 1))
        self.assertFalse(tests.meets_requirements("Pass1.", 2, 1, 1, 1))

    def test_notSQL(self):

        self.assertTrue(tests.notSQL("This is not SQL"))

        self.assertFalse(tests.notSQL("DROP DATABASE Brukersys"))


class testAdmin(unittest.TestCase):

    def test_isAdmin(self):
        self.assertTrue(sqlf.isAdministrator('Bruker1'))
        self.assertFalse(sqlf.isAdministrator('testbruker'))


class testSQL(unittest.TestCase):

    def test_checkpass(self):

        self.assertTrue(sqlf.check_password('Bruker1', '123'))

        self.assertFalse(sqlf.check_password('Bruker1', '123efwef.'))

    def test_addUser(self):

        self.assertEqual(sqlf.add_user(
            'DROP DATABASE 123', '123'), PermissionError)
        self.assertEqual(sqlf.add_user('bruker421', '123'), PermissionError)
        self.assertEqual(sqlf.add_user(
            'bruker421', 'Potet123'), PermissionError)
