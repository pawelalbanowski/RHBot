class Divisions:
    def __init__(self):
        self._d1 = 548999
        self._d2 = 559999
        self._d3 = 0

    @property
    def d1(self):
        return self._d1

    @property
    def d2(self):
        return self._d2

    @property
    def d3(self):
        return self._d3

    def check_laptime(self, lap):
        if lap <= self._d1:
            return 'D1'
        elif lap <= self._d2:
            return 'D2'
        return 'D3'