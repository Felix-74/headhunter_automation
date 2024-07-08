class ParkChecking:
    park_set = set()

    @classmethod
    def parking(cls, car_id: int, n) -> bool | None:
        if len(cls.park_set) < n:
            cls.park_set.add(car_id)
            print(f'Car{car_id} has parked')
            return True
        else:
            print('parking is full')
            return False

    @classmethod
    def unparking(cls, car_id: int) -> bool | None:
        if car_id in cls.park_set:
            cls.park_set.remove(car_id)
            print(f'Car{car_id} has removed')
        else:
            print(f'Car{car_id} not in parking')

n = 5
print(ParkChecking.parking("ABC123", n))
print(ParkChecking.parking("ABC124", n))
print(ParkChecking.parking("ABC125", n))
print(ParkChecking.parking("ABC126", n))
print(ParkChecking.parking("ABC127", n))
print(ParkChecking.parking("ABC123", n))
print(ParkChecking.parking("ABC126", n))