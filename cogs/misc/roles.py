from pprint import pprint

class Roles:
    def __init__(self):
        self._member = 884810404415541329
        self._admin = 880617302410809424
        self._staff = 977273637226819744
        self._driver = 875743731536510987
        self._div_manager = 1020381074905378917
        self._cars = {
            'Porsche': 1066758489206169623,
            'Mercedes': 1066758512530698314,
            'Chevrolet': 1066758534139740190,
            'Aston Martin': 1066758558651261038,
            'Ford': 1066758583158591591
        }
        self._leagues = {
            'D1': 930024457446232095,
            'D2': 930024502442729492,
            'D3': 940646795044851742
        }
        self._quali = {
            1 : 1008283782874415134,
            2 : 1008283856622850048,
            3 : 1008283873005797376,
            4 : 1008283885332869132,
            5 : 1008283896422617220,
            6 : 1008283906342129735,
            7 : 1072164494215762030,
            8 : 1072164516051308738,
        }

    @property
    def member(self):
        return self._member

    @property
    def admin(self):
        return self._admin

    @property
    def staff(self):
        return self._staff

    @property
    def driver(self):
        return self._driver

    @property
    def cars(self):
        return self._cars

    @property
    def leagues(self):
        return self._leagues

    @property
    def div_manager(self):
        return self._div_manager

    @property
    def quali_specific(self, number):
        return self._quali.get(number)

    @property
    def quali(self):
        return self._quali







