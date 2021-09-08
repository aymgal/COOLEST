

class Redshift(object):

    def __init__(self, 
                 z: float) -> None:
        if z < 0:
            raise ValueError("Redshift cannot be negative.")
        self.z = z
