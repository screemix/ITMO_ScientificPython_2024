import openmeteo_requests
import datetime

class IncreaseSpeed():

  def __init__(self, current_speed: int, max_speed: int):
    self.current_speed = current_speed
    self.max_speed = max_speed

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current_speed == self.max_speed:
      raise StopIteration
    
    self.current_speed = min(self.current_speed + 10, self.max_speed)
    return self.current_speed


class DecreaseSpeed():

  def __init__(self, current_speed: int, min_speed: int):
    self.current_speed = current_speed
    self.min_speed = min_speed

  def __iter__(self):
    return self
  
  def __next__(self):
    if self.current_speed == self.min_speed:
      raise StopIteration
    else: 
        self.current_speed = max(self.current_speed - 10, self.min_speed)
    return self.current_speed


class Car():

    num_cars = 0

    def __init__(self, max_speed: int, current_speed=0):
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.state = True
        Car.num_cars += 1
    

    def accelerate(self, upper_border=None):

        if not self.state:
            self.state = True

        if isinstance(upper_border, int):
            speed_iterator = IncreaseSpeed(self.current_speed, min(upper_border, self.max_speed))

            for step in iter(speed_iterator):
                print("Increasing speed, current speed is {}...".format(self.current_speed))
                self.current_speed = step
                
            
            print("Increased speed, current speed is {}".format(self.current_speed))

        elif self.current_speed < self.max_speed:
            speed_iterator = IncreaseSpeed(self.current_speed, self.max_speed)
            self.current_speed = next(speed_iterator)
            print("Increased speed, current speed is {}...".format(self.current_speed))

        return self.current_speed
            


    def brake(self, lower_border=None):

        if isinstance(lower_border, int):
            speed_iterator = DecreaseSpeed(self.current_speed, max(lower_border, 0))

            for step in iter(speed_iterator):
                print("Decreasing speed, current speed is {}...".format(self.current_speed))
                self.current_speed = step
            
            print("Decreased speed, current speed is {}".format(self.current_speed))
                
        elif 0 < self.current_speed:
            speed_iterator = DecreaseSpeed(self.current_speed, 0)
            self.current_speed = next(speed_iterator)
            print("Decreased speed, current speed is {}...".format(self.current_speed))

        return self.current_speed


    def parking(self):
        if self.state:
           self.state = False
           self.current_speed = 0
           Car.num_cars -= 1

    @classmethod
    def total_cars(Car):
        return Car.num_cars
    
    @staticmethod
    def show_weather():
        openmeteo = openmeteo_requests.Client()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude": 59.9386, # for St.Petersburg
        "longitude": 30.3141, # for St.Petersburg
        "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
        }
        response = openmeteo.weather_api(url, params=params)[0]
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_rain = current.Variables(2).Value()
        current_wind_speed_10m = current.Variables(3).Value()

        print(f"Current time: {datetime.datetime.fromtimestamp(current.Time()+response.UtcOffsetSeconds())} {response.TimezoneAbbreviation().decode()}")
        print(f"Current temperature: {round(current_temperature_2m, 0)} C")
        print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
        print(f"Current rain: {current_rain} mm")
        print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")