from aocd import data


def parse_location(curr_loc_string):
    """
    takes in a single location (either sensor or beacon) and returns the location as a tuple
    :param curr_loc_string: string in the format "Sensor at x=9, y=16"
    :return: tuple of location

    >>> parse_location("Sensor at x=9, y=16")
    (9, 16)

    >>> parse_location("closest beacon is at x=10, y=16")
    (10, 16)
    """
    loc_ls = curr_loc_string.split("at ")[1].split(", ")
    loc_tuple = tuple([int(x.split("=")[1]) for x in loc_ls])
    return loc_tuple


def parse_row(curr_string):
    """
    takes in a string and extracts the sensor/beacon location pair
    :param curr_string: raw input string in the format "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
    :return: tuple of sensor/beacon locations

    example usage:
    >>> parse_row("Sensor at x=2, y=18: closest beacon is at x=-2, y=15")
    ((2, 18), (-2, 15))

    """
    split_row = curr_string.split(": ")
    sensor_beacon_loc_tuple = tuple(map(parse_location, split_row))

    return sensor_beacon_loc_tuple


def parse_input(raw_input):
    """
    takes in the raw data and returns as tuples of sensor/beacon locations
    :param raw_input: raw_input
    :return: tuple of tuples of sensor/beacon locations
    """
    split_input = raw_input.split("\n")
    locations_tuple = tuple(map(parse_row, split_input))
    return locations_tuple


def find_manhattan_distance(sensor_tuple, beacon_tuple):
    """
    given a pair of locations, calculates the manhattan distance between them
    :param sensor_tuple: location of the sensor
    :param beacon_tuple: location of the beacon
    :return: manhattan distance between the two locations

    >>> find_manhattan_distance((8,7),(2,10))
    9

    >>> find_manhattan_distance((0,11),(2,10))
    3
    """
    manhattan_distance = abs(sensor_tuple[0] - beacon_tuple[0]) + abs(sensor_tuple[1] - beacon_tuple[1])
    return manhattan_distance


def excluded_row_positions(center_posn, horiz_distance, max_value=None):
    """
    Finds range of  excluded positions in a row given the center position and the distance from the center
    :param max_value: maximum acceptable x value.  also sets the minimum value ot 0.  If omitted, allows all values
    :param center_posn: center position of the row
    :param horiz_distance: distance from the center to exclude
    :return: range of excluded positions in the row

    >>> excluded_row_positions((0,8),0)
    (0, 0)

    >>> excluded_row_positions((0,10), 2)
    (-2, 2)

    >>> excluded_row_positions((0,10), 2, 1)
    (0, 1)

    """
    center_x_posn = center_posn[0]

    if max_value:
        range_min = 0 if center_x_posn - horiz_distance < 0 else center_x_posn - horiz_distance
        range_max = max_value if center_x_posn + horiz_distance + 1 > max_value else center_x_posn + horiz_distance
        return range_min, range_max

    else:
        return center_x_posn - horiz_distance, center_x_posn + horiz_distance


def find_excluded_range(sensor_tuple, manhattan_distance, y_row, max_value=None):
    """
    given a sensor locations, returns the range of positions that are within a specified distance from it
    :param max_value: maximum acceptable x value.  also sets the minimum value ot 0.  If omitted, allows all values
    :param y_row: row to limit positions to
    :param sensor_tuple: location of sensor
    :param manhattan_distance: distance from sensor
    :return: range of min,max values that should be excluded

    >>> find_excluded_range((0,11),3,10)
    (-2, 2)

    >>> find_excluded_range((0,10), 2, 10, 1)
    (0, 1)
    """

    sensor_x = sensor_tuple[0]
    sensor_y = sensor_tuple[1]

    # calculate distance between y_row and sensor
    y_dist = abs(sensor_y - y_row)

    excluded_position_range = excluded_row_positions(
        (sensor_x, y_row),
        manhattan_distance - y_dist,
        max_value
    )

    return excluded_position_range


def exclude_positions(location_tuple, y_row, max_value=None):
    """
    given a sensor/beacon location, determines the range of positions that cannot contain a beacon that are within y_row
    :param y_row: row to limit positions to
    :param max_value: maximum acceptable x value.  also sets the minimum value ot 0.  If omitted, allows all values
    :param location_tuple: location to analyze
    :return: range of excluded positions in the row

    >>> exclude_positions(((0,11),(2,10)),10)
    (-2, 2)

    >>> exclude_positions(((0,11),(2,10)),10, 1)
    (0, 1)
    """
    sensor_tuple = location_tuple[0]
    beacon_tuple = location_tuple[1]

    manhattan_distance = find_manhattan_distance(sensor_tuple, beacon_tuple)
    excluded_range = find_excluded_range(sensor_tuple, manhattan_distance, y_row, max_value)

    return excluded_range


def is_crossing(curr_tuple, y_row):
    """
    does the current sensor/beacon tuple cross y_row?
    :param curr_tuple: sensor/beacon tuple
    :param y_row: horizontal row that needs to be crossed
    :return: bool if the curr_tuple crosses y_row

    >>> is_crossing(((2, 18), (-2, 15)), 10)
    False
    >>> is_crossing(((9, 16), (10, 16)), 10)
    False
    >>> is_crossing(((13, 2), (15, 3)), 10)
    False
    >>> is_crossing(((12, 14), (10, 16)), 10)
    True
    >>> is_crossing(((10, 20), (10, 16)), 10)
    False
    >>> is_crossing(((14, 17), (10, 16)), 10)
    False
    >>> is_crossing(((8, 7), (2, 10)), 10)
    True
    >>> is_crossing(((2, 0), (2, 10)), 10)
    True
    >>> is_crossing(((0, 11), (2, 10)), 10)
    True
    >>> is_crossing(((20, 14), (25, 17)), 10)
    True
    >>> is_crossing(((17, 20), (21, 22)), 10)
    False
    >>> is_crossing(((16, 7), (15, 3)), 10)
    True
    >>> is_crossing(((14, 3), (15, 3)), 10)
    False
    >>> is_crossing(((20, 1), (15, 3)), 10)
    False
    """

    sensor_tuple_y = curr_tuple[0][1]
    beacon_tuple_y = curr_tuple[1][1]

    if (sensor_tuple_y == y_row) or (beacon_tuple_y == y_row):  # if either beacon or sensor is on y_row
        return True
    elif (
            (sensor_tuple_y < y_row) and (beacon_tuple_y > y_row) or
            (sensor_tuple_y > y_row) and (beacon_tuple_y < y_row)
    ):  # y_row is between the sensor and beacon rows
        return True
    else:
        manhattan_distance = find_manhattan_distance(*curr_tuple)
        if (sensor_tuple_y - manhattan_distance <= y_row) and (
                sensor_tuple_y + manhattan_distance >= y_row):  # y_row is within manhattan_distance from the sensor
            return True
        else:  # sensor pair does not cross y_row
            return False


def crossing_locations(locations_tuple, y_row):
    """
    given a tuple of locations, determines how many of them cross the given y-location
    :param locations_tuple: list of sensor/beacon locations
    :param y_row: y-row to investigate
    :return: tuple of locations that cross y_row

    >>> crossing_locations((((2, 18), (-2, 15)),((9, 16), (10, 16)), ((13, 2), (15, 3)),((12, 14), (10, 16)),((10, 20), (10, 16)),((14, 17), (10, 16)),((8, 7), (2, 10)),((2, 0), (2, 10)),((0, 11), (2, 10)),((20, 14), (25, 17)),((17, 20), (21, 22)),((16, 7), (15, 3)),((14, 3), (15, 3)),((20, 1), (15, 3))),10)
    (((12, 14), (10, 16)), ((8, 7), (2, 10)), ((2, 0), (2, 10)), ((0, 11), (2, 10)), ((20, 14), (25, 17)), ((16, 7), (15, 3)))
    """
    crossing_locations_tuple = tuple([x for x in locations_tuple if is_crossing(x, y_row)])
    return crossing_locations_tuple


def is_overlapping_range(range_1, range_2):
    """
    determines if two ranges are overlapping
    :param range_1: first range to compare
    :param range_2: second range to compare
    :return: bool if ranges are overlapping

    >>> is_overlapping_range((12,12),(12,14))
    True

    >>> is_overlapping_range((12,12),(10,12))
    True

    >>> is_overlapping_range((12,16),(10,14))
    True

    >>> is_overlapping_range((12,16),(14,18))
    True

    >>> is_overlapping_range((12,16),(12,14))
    True

    >>> is_overlapping_range((12,16),(16,18))
    True

    >>> is_overlapping_range((12,16),(10,12))
    True

    >>> is_overlapping_range((4,16),(10,12))
    True

    >>> is_overlapping_range((12,16),(13,14))
    True

    >>> is_overlapping_range((11,11),(10,12))
    True

    >>> is_overlapping_range((12,16),(14,14))
    True

    >>> is_overlapping_range((12,16),(14,16))
    True

    >>> is_overlapping_range((12,16),(12,18))
    True

    >>> is_overlapping_range((10,13),(14,18))
    False
    """
    if (range_1[0] >= range_2[0]) and (range_1[0] <= range_2[1]):
        return True
    elif (range_1[1] >= range_2[0]) and (range_1[1] <= range_2[1]):
        return True
    elif (range_1[0] >= range_2[0]) and (range_1[1] <= range_2[1]):
        return True
    elif (range_1[1] >= range_2[1]) and (range_1[0] <= range_2[0]):
        return True
    else:
        return False


def extend_ranges(new_range, overlapping_ranges):
    """
    extends the ranges in overlapping ranges by new_range
    :param new_range: single range that overlaps each range in overlapping ranges
    :param overlapping_ranges: set of ranges that overlap new_range
    :return: set of ranges extended by new_range

    >>> extend_ranges((5,10),{(1,5),(10,20),(2,7),(8,15)}) == {(1, 10), (5, 20), (2, 10), (5, 15)}
    True
    """
    processed_ranges = set()
    for curr_range in overlapping_ranges:
        range_min = curr_range[0] if curr_range[0] <= new_range[0] else new_range[0]
        range_max = curr_range[1] if curr_range[1] >= new_range[1] else new_range[1]
        processed_ranges.add((range_min, range_max))
    return processed_ranges


def range_collapse(new_range, excluded_ranges_set):
    """
    given a range and a set of ranges, collapses overlapping ranges into single ranges
    :param new_range: new range to consider adding to set of ranges
    :param excluded_ranges_set: set of previously defined ranges
    :return: updated excluded_ranges_set

    >>> range_collapse((5, 10), {(1, 2), (15, 20)})== {(1, 2), (15, 20), (5, 10)}
    True

    >>> range_collapse((5, 10), {(1, 5), (15, 20)})== {(1, 10), (15, 20)}
    True

    >>> range_collapse((20, 30), {(1, 2), (15, 20)})== {(1, 2), (15, 30)}
    True

    >>> range_collapse((17, 30), {(1, 2), (15, 20)})== {(1, 2), (15, 30)}
    True

    >>> range_collapse((3, 17), {(1, 2), (15, 20)})== {(1, 2), (3, 20)}
    True

    >>> range_collapse((3, 17), {(1, 5), (15, 20)})== {(1, 20)}
    True
    """
    overlapping_ranges = {range_tuple for range_tuple in excluded_ranges_set if
                          is_overlapping_range(new_range, range_tuple)}
    non_overlapping_ranges = excluded_ranges_set.difference(overlapping_ranges)
    if overlapping_ranges:
        # extend the existing ranges by new_range
        processed_ranges = extend_ranges(new_range, overlapping_ranges)
        # do any of the extended ranges overlap with each other?
        overlapping_processed_ranges = {range_tuple for range_tuple in processed_ranges if sum(
            {is_overlapping_range(range_1, range_tuple) for range_1 in processed_ranges.difference({range_tuple})}) > 0}
        while overlapping_processed_ranges:
            curr_range = next(iter(overlapping_processed_ranges))  # first item in set
            processed_ranges = extend_ranges(curr_range, overlapping_processed_ranges.difference({curr_range}))
            overlapping_processed_ranges = {range_tuple for range_tuple in processed_ranges if sum(
                {is_overlapping_range(range_1, range_tuple) for range_1 in
                 processed_ranges.difference({range_tuple})}) > 0}
        return processed_ranges.union(non_overlapping_ranges)
    else:
        excluded_ranges_set.add(new_range)
        return excluded_ranges_set


def beacon_exclusion(raw_input, y_row):
    """
    takes the raw data and determines how many positions in a given row cannot have a beacon
    :param y_row: row to investigate
    :param raw_input: raw input of sensor and beacon locations
    :return: number of positions in y_row that cannot contain a beacon
    """
    locations_tuple = parse_input(raw_input)

    row_locations_tuple = crossing_locations(locations_tuple, y_row)  # limit to only positions that cross y_row

    excluded_ranges_set = set()

    for curr_pair in row_locations_tuple:
        new_range = exclude_positions(curr_pair, y_row)
        # does this new range_tuple overlap a range_tuple in the set? if so, collapse
        excluded_ranges_set = range_collapse(new_range, excluded_ranges_set)

    return sum([x[1] - x[0] for x in excluded_ranges_set])


def find_tuning_frequency(raw_input, max_value):
    """
    given
    :param max_value: maximum value for either x or y coordinate
    :param raw_input: raw input of sensor and beacon locations
    :return: tuning frequency
    """
    locations_tuple = parse_input(raw_input)

    # check each row
    for row_num in range(max_value + 1):
        if row_num % 100000 == 0:
            print(row_num)
        row_locations_tuple = crossing_locations(locations_tuple, row_num)
        excluded_ranges_set = set()
        for curr_pair in row_locations_tuple:
            new_range = exclude_positions(curr_pair, row_num, max_value)
            # does this new range_tuple overlap a range_tuple in the set? if so, collapse
            excluded_ranges_set = range_collapse(new_range, excluded_ranges_set)

        if len(excluded_ranges_set) > 1:  # the range is discontinuous
            sorted_range = sorted(excluded_ranges_set)
            x_posn = sorted_range[0][1] + 1
            tuning_frequency = (x_posn * 4000000) + row_num
            return tuning_frequency


if __name__ == '__main__':
    print(f"There are {beacon_exclusion(data, 2000000)} positions on row y=2000000 that cannot contain a beacon")
    print(f"The tuning frequency of the distress beacon is {find_tuning_frequency(data, 4000000)}")
