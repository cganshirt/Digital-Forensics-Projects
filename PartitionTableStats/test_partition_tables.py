import unittest
from uuid import UUID


import partition_tables


class TestParseMBR(unittest.TestCase):
    def testSimpleMBR(self):
        with open('usb-mbr.dd', 'rb') as f:
            data = f.read(512)
        self.assertEqual([{'type': '0x6', 'end': 3913727, 'start': 32, 'number': 0}],
                         partition_tables.parse_mbr(data))

    def testTestMBR(self):
        with open('test-mbr.dd', 'rb') as f:
            data = f.read(512)
        self.assertEqual([{'type': '0x4', 'end': 6143, 'start': 2048, 'number': 0},
                          {'type': '0x83', 'end': 14335, 'start': 6144, 'number': 1},
                          {'type': '0x8e', 'end': 30719, 'start': 14336, 'number': 2},
                          {'type': '0x82', 'end': 40959, 'start': 30720, 'number': 3}],
                         partition_tables.parse_mbr(data))


class TestParseGPT(unittest.TestCase):
    def testSimpleGPT(self):
        with open('disk-image.dd', 'rb') as f:
            self.assertEqual([{'start': 40, 'end': 409639, 'number': 0, 'name': 'EFI system partition',
                               'type': UUID('c12a7328-f81f-11d2-ba4b-00a0c93ec93b')},
                              {'start': 409640, 'end': 585210495, 'number': 1, 'name': 'Iron',
                               'type': UUID('53746f72-6167-11aa-aa11-00306543ecac')},
                              {'start': 585210496, 'end': 586480031, 'number': 2, 'name': 'Recovery HD',
                               'type': UUID('426f6f74-0000-11aa-aa11-00306543ecac')},
                              {'start': 586481664, 'end': 976842879, 'number': 3, 'name': 'Apple_HFS_Untitled_2',
                               'type': UUID('48465300-0000-11aa-aa11-00306543ecac')}],
                             partition_tables.parse_gpt(f, 512))

    def testTestGPT(self):
        with open('test-gpt.dd', 'rb') as f:
            self.assertEqual([{'number': 0, 'name': 'EFI system partition', 'end': 12287,
                               'type': UUID('c12a7328-f81f-11d2-ba4b-00a0c93ec93b'), 'start': 2048},
                              {'number': 1, 'name': 'Windows recovery environment', 'end': 32767,
                               'type': UUID('de94bba4-06d1-4d40-a16a-bfd50179d6ac'), 'start': 12288},
                              {'number': 2, 'name': 'Linux root (x86-64)', 'end': 53247,
                               'type': UUID('4f68bce3-e8cd-4db1-96e7-fbcaf984b709'), 'start': 32768},
                              {'number': 3, 'name': 'Linux swap', 'end': 69631,
                               'type': UUID('0657fd6d-a4ab-43c4-84e5-0933c84b4f4f'), 'start': 53248},
                              {'number': 4, 'name': 'Linux LVM', 'end': 204766,
                               'type': UUID('e6d6d379-f507-44c2-a23c-238f2a3df928'), 'start': 69632}],
                             partition_tables.parse_gpt(f, 512))


if __name__ == '__main__':
    unittest.main()
