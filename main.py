import sys
import json


def point_in_polygon(point: list, polygon: list):
    x = point[0]
    y = point[1]

    n = len(polygon)
    inside = False

    for i in range(n):
        # Get the current vertex in the polygon
        coordinates1 = polygon[i]
        x1 = coordinates1[0]
        y1 = coordinates1[1]

        # Get the next vertex in the polygon
        # If the current vertex is the last one, get the first vertex (polygon is closed)
        coordinates2 = polygon[(i + 1) % n]
        x2 = coordinates2[0]
        y2 = coordinates2[1]

        if (y1 < y <= y2) or (y2 < y <= y1):
            intersection_x = x1 + (y - y1) / (y2 - y1) * (x2 - x1)
            if intersection_x < x:
                inside = not inside

    return inside


def parse_command(command: list):
    pg_mode, rg_path, lc_path, rs_path = "1", None, None, None
    command = command[1:]
    for i in range(len(command)):
        arg = command[i]
        if arg.startswith("--mode"):
            pg_mode = arg.split("=")[1]
        elif arg.startswith("--regions"):
            rg_path = arg.split("=")[1]
        elif arg.startswith("--locations"):
            lc_path = arg.split("=")[1]
        elif arg.startswith("--output"):
            rs_path = arg.split("=")[1]

    return pg_mode, rg_path, lc_path, rs_path


def get_results_for_region(regions_list: list, locations_list: list):
    results = []
    for region in regions_list:
        matched_locations = []

        for location in locations_list:
            for polygon in region['coordinates']:
                if point_in_polygon(location['coordinates'], polygon):
                    matched_locations.append(location['name'])
                    break

        results.append({
            'region': region['name'],
            'matched_locations': matched_locations
        })

    return results


def get_results_for_location(regions_list: list, locations_list: list):
    results = []
    for location in locations_list:
        matched_regions = []

        for region in regions_list:
            for polygon in region['coordinates']:
                if point_in_polygon(location['coordinates'], polygon):
                    matched_regions.append(region['name'])
                    break

        results.append({
            'location': location['name'],
            'matched_regions': matched_regions
        })

    return results


def run_program():
    (program_mode, regions_path, locations_path, results_path) = parse_command(sys.argv)

    if regions_path is None or locations_path is None or results_path is None:
        print("Usage: python main.py --mode=mode --regions=path --locations=path --output=path")
        sys.exit(1)

    with open(regions_path, 'r') as regions_file:
        regions = json.loads(regions_file.read())

    with open(locations_path, 'r') as locations_file:
        locations = json.loads(locations_file.read())

    with open(results_path, 'w') as results_file:
        if program_mode == "1":
            results_file.write(json.dumps(get_results_for_region(regions, locations), indent=2))
        elif program_mode == "2":
            results_file.write(json.dumps(get_results_for_location(regions, locations), indent=2))
        else:
            print("Invalid mode. Use 1 for regions with locations OR 2 for locations with regions.")
            sys.exit(1)

    print("Results saved to", results_path)


if __name__ == '__main__':
    run_program()
