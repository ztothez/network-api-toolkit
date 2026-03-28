import json
import time
import urllib.parse
import urllib.request

import pgeocode


ASTROS_URL = "http://api.open-notify.org/astros.json"
ISS_NOW_URL = "http://api.open-notify.org/iss-now.json"
ISS_PASS_URL = "http://api.open-notify.org/iss-pass.json"


def fetch_json(url: str):
    """Fetch JSON data from a URL."""
    with urllib.request.urlopen(url) as response:
        return json.loads(response.read())


def get_people_in_space():
    """Return the current number of people in space and their spacecraft."""
    result = fetch_json(ASTROS_URL)
    return result["number"], result["people"]


def get_iss_current_location():
    """Return the ISS current latitude and longitude."""
    result = fetch_json(ISS_NOW_URL)
    location = result["iss_position"]
    return float(location["latitude"]), float(location["longitude"])


def get_iss_passes(lat: float, lon: float):
    """Return upcoming ISS passes for a given latitude and longitude."""
    query = urllib.parse.urlencode({"lat": lat, "lon": lon})
    result = fetch_json(f"{ISS_PASS_URL}?{query}")
    return result["request"]["passes"], result["response"]


def get_coordinates_from_postal_code(country_code: str, postal_code: str):
    """Return latitude and longitude from a postal code using pgeocode."""
    nomi = pgeocode.Nominatim(country_code)
    place = nomi.query_postal_code(postal_code)

    if place is None or place.empty:
        return None, None

    lat = place.latitude
    lon = place.longitude

    if lat is None or lon is None:
        return None, None

    return float(lat), float(lon)


def print_people_in_space():
    number, people = get_people_in_space()
    print(f"People in Space: {number}\n")
    for person in people:
        print(f"{person['name']} - {person['craft']}")


def print_iss_location():
    lat, lon = get_iss_current_location()
    print(f"\nISS current location: {lat} {lon}")
    return lat, lon


def print_passes_for_location(name: str, lat: float, lon: float):
    print(f"\nISS pass information for {name}")
    print(f"Latitude: {lat}, Longitude: {lon}")

    passes_count, passes = get_iss_passes(lat, lon)
    print(f"\nPasses for today: {passes_count}\n")
    print("Duration means pass length in seconds.\n")

    for item in passes:
        print(
            f"The duration is: {item['duration']}\n"
            f"The risetime is: {time.ctime(item['risetime'])}\n"
        )

    if len(passes) > 1:
        next_pass = time.ctime(passes[1]["risetime"])
        print(f"Next visible pass for {name}: {next_pass}")


def draw_turtle_map(iss_lat: float, iss_lon: float, target_lat: float, target_lon: float, next_pass_time: str):
    """Optional turtle map display."""
    import turtle

    screen = turtle.Screen()
    screen.setup(720, 360)
    screen.setworldcoordinates(-180, -90, 180, 90)
    screen.bgpic("map.gif")

    screen.register_shape("iss.gif")
    iss = turtle.Turtle()
    iss.shape("iss.gif")
    iss.setheading(90)
    iss.penup()
    iss.goto(iss_lon, iss_lat)

    location = turtle.Turtle()
    location.penup()
    location.color("yellow")
    location.goto(target_lon, target_lat)
    location.dot(5)
    location.hideturtle()

    style = ("arial", 6, "bold")
    location.write(next_pass_time, font=style)

    turtle.done()


def main():
    print_people_in_space()

    iss_lat, iss_lon = print_iss_location()

    # Show ISS passes at its current coordinates
    print_passes_for_location("current ISS position", iss_lat, iss_lon)

    # Default location: Turku
    turku_lat = 60.4518
    turku_lon = 22.2666
    print_passes_for_location("Turku", turku_lat, turku_lon)

    # Optional user input
    use_custom_location = input("\nDo you want to check another location by postal code? (y/n): ").strip().lower()

    custom_lat = None
    custom_lon = None
    custom_name = None

    if use_custom_location == "y":
        country_code = input("Add country code: ").strip()
        postal_code = input("Add postal code: ").strip()

        custom_lat, custom_lon = get_coordinates_from_postal_code(country_code, postal_code)

        if custom_lat is not None and custom_lon is not None:
            custom_name = f"{country_code.upper()} {postal_code}"
            print_passes_for_location(custom_name, custom_lat, custom_lon)
        else:
            print("Could not find coordinates for that postal code.")

    # Optional turtle map
    use_map = input("\nDo you want to open the turtle map view? (y/n): ").strip().lower()
    if use_map == "y":
        target_lat = custom_lat if custom_lat is not None else turku_lat
        target_lon = custom_lon if custom_lon is not None else turku_lon

        _, passes = get_iss_passes(target_lat, target_lon)
        next_pass_time = time.ctime(passes[1]["risetime"]) if len(passes) > 1 else "No pass data available"

        draw_turtle_map(iss_lat, iss_lon, target_lat, target_lon, next_pass_time)


if __name__ == "__main__":
    main()