import unittest
from main import UserRegister, get_list_of_files


class TestUserRegister(unittest.TestCase):
    def setUp(self):
        list_of_files = get_list_of_files('users')
        self.ur = UserRegister(list_of_files)

    def test_set_name_surname(self):
        with self.subTest():
            result = self.ur.set_name_username('jelena.kovacevic@rt-rk.com', 'Jelena Kovacevic')
            self.assertEqual('jelena.kovacevic@rt-rk.com', result, 'First test failed!')
        with self.subTest():
            result = self.ur.set_name_username('pero.peric@rt-rk.com', 'Pero Peric')
            self.assertEqual(None, result, 'Second test failed!')

    def test_validate_ip_address(self):
        with self.subTest():
            result = self.ur.validate_ip_address('192.168.100.1')
            self.assertEqual(True, result, 'First test failed!')
        with self.subTest():
            result = self.ur.validate_ip_address('192.168.100')
            self.assertEqual(False, result, 'Second test failed!')

    def test_get_user(self):
        with self.subTest():
            result = self.ur.get_user('nikola.jeftenic@rt-rk.com')
            self.assertEqual(dict(name='Nikola Jeftenic', email='nikola.jeftenic@rt-rk.com', ip='192.168.100.1',
                                  devices=['desktop RTRK-1', 'mobile MB-1', 'desktop RTRK-12', 'mobile MB-11']),
                             result, 'First test failed!')
        with self.subTest():
            result = self.ur.get_user('pero.peric@rt-rk.com')
            self.assertEqual('No one is associated with pero.peric@rt-rk.com', result, 'Second test failed!')

    def test_get_ip(self):
        with self.subTest():
            result = self.ur.get_ip('nedo.todoric@rt-rk.com')
            self.assertEqual('192.168.100.3', result, 'First test failed!')
        with self.subTest():
            result = self.ur.get_ip('pero.peric@rt-rk.com')
            self.assertEqual('No IP associated with pero.peric@rt-rk.com', result, 'Second test failed!')

    def test_get_name_surname(self):
        with self.subTest():
            result = self.ur.get_name_surname('djordje.bogdanic@rt-rk.com')
            self.assertEqual('Djordje Bogdanic', result, 'First test failed!')
        with self.subTest():
            result = self.ur.get_name_surname('pero.peric@rt-rk.com')
            self.assertEqual('No one is associated with pero.peric@rt-rk.com', result, 'Second test failed!')

    def test_get_devices(self):
        with self.subTest():
            result = self.ur.get_devices('nedo.todoric@rt-rk.com')
            self.assertEqual(['desktop RTRK-3', 'mobile MB-3'], result, 'First test failed!')
        with self.subTest():
            result = self.ur.get_devices("greska.greska@rt-rk.com")
            self.assertEqual('No devices associated with greska.greska@rt-rk.com', result, 'Second test failed!')

    def test_set_devices(self):
        with self.subTest():
            result = self.ur.set_devices('jelena.kovacevic@rt-rk.com', ["desktop RTRK-2", "mobile MB-2"])
            self.assertEqual(['desktop RTRK-2', 'mobile MB-2'], result, 'First test failed!')
        with self.subTest():
            result = self.ur.set_devices('pero.peric@rt-rk.com', ["desktop RTRK-2", "mobile MB-2"])
            self.assertEqual('No devices associated with pero.peric@rt-rk.com', result, 'Second test failed!')
        with self.subTest():
            result = self.ur.set_devices('jelena.kovacevic@rt-rk.com', ["RTRK-2", "mobile MB-2"])
            self.assertEqual('Device tags are not valid!', result, 'Third test failed!')

    def test_set_ip(self):
        with self.subTest():
            result = self.ur.set_ip('jelena.kovacevic@rt-rk.com', '192.168.100.12')
            self.assertEqual('192.168.100.12', result, 'First test failed!')
        with self.subTest():
            result = self.ur.set_ip('jelena.kovacevic@rt-rk.com', '12.21.')
            self.assertEqual(None, result, 'Second test failed!')
        with self.subTest():
            result = self.ur.set_ip('jelenart-rk.com', '192.168.100.12')
            self.assertEqual(None, result, 'Second test failed!')

    def test_check_email(self):
        with self.subTest():
            result = self.ur.check_email('jelena.kovacevic@rt-rk,com')
            self.assertEqual(True, result, 'First test failed!')
        with self.subTest():
            result = self.ur.check_email('jelenart-rk.com')
            self.assertEqual(False, result, 'Second test failed!')
            