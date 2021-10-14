from datetime import date


class Building:

    def __init__(self, price, address, building_type, year_built=0, floors=0, postal_code='', lot_info='', mls_number=0,
                 description='', province='', city=''):
        self.price = price
        self.address = address
        self.build_type = building_type
        self.year_built = year_built
        self.floors = floors
        self.postal_code = postal_code
        self.lot_info = lot_info
        self.mls_number = mls_number
        self.description = description
        self.date = date.today()
        self.province = province
        self.city = city