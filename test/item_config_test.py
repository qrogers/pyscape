# Creates every item to verify they have valid config

import unittest

from bin.inventory_handler import InventoryHandler

class ItemConfigTest(unittest.TestCase):

    def test_all_items(self):
        inventory_handler = InventoryHandler