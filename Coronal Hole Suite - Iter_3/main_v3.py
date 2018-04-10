import parse_discovr_data
import parse_solar_image

discovr = parse_discovr_data.SatelliteDataProcessor()
sun = parse_solar_image.SolarImageProcessor()

if __name__ == "__main__":
    discovr.get_data()
    sun.get_meridian_coverage()
