

class Temperature:
    def __init__(self, temperature):
        self.temperature = temperature  

    @property
    def temperature(self):
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if not (-273.15 <= value <= 5000):
            raise ValueError("Temperature must be between -273.15°C and 5000°C.")
        self._temperature = value

    def __str__(self):
        return f"{self.temperature}°C"

if __name__ == '__main__':
    try:
        temp = Temperature(25)
        print(temp)
        temp.temperature = 6000  
    except ValueError as e:
        print("Error:", e)
