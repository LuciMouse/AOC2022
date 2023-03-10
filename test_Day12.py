import unittest
import Day12


class TestIsAcessible(unittest.TestCase):
    def test_is_acessible(self):
        with open("Day12_test_input.txt") as input_file:
            raw_data = input_file.read()
        height_map_ls = [[*row] for row in raw_data.split('\n')]
        self.assertEqual(
            [
                (0, 1),
                (1, 0),
                None,
                (1, 2),
                (1, 2),
                None,
                (0, 1),

            ],
            [x.coord if x else None for x in
             [
                 Day12.is_acessible(Day12.create_node((0, 0), height_map_ls), (0, 1), height_map_ls, {}),
                 # child_elevation == 'a'
                 Day12.is_acessible(Day12.create_node((0, 0), height_map_ls), (1, 0), height_map_ls, {}),
                 # child_elevation == 'a'
                 Day12.is_acessible(Day12.create_node((0, 0), height_map_ls), (1, 2), height_map_ls, {}),
                 # child_elevation == 'c'
                 Day12.is_acessible(Day12.create_node((1, 1), height_map_ls), (1, 2), height_map_ls, {}),
                 # child_elevation == 'c'
                 Day12.is_acessible(Day12.create_node((4, 3), height_map_ls), (1, 2), height_map_ls, {}),
                 # child_elevation == 'c'
                 Day12.is_acessible(Day12.create_node((3, 5), height_map_ls), (2, 4), height_map_ls, {}),
                 # child_elevation == 'z'
                 Day12.is_acessible(Day12.create_node((0, 0), height_map_ls), (0, 1), height_map_ls,
                                    {(0, 1): Day12.create_node((0, 1), height_map_ls)})  # child_elevation == 'a'
             ]
             ]
        )


class TestCheckChildren(unittest.TestCase):
    def test_check_children(self):
        with open("Day12_test_input.txt") as input_file:
            raw_data = input_file.read()
        height_map_ls = [[*row] for row in raw_data.split('\n')]
        curr_node = Day12.create_node(
            (0, 0),
            height_map_ls
        )
        child_nodes = [
            Day12.create_node((0, 1), height_map_ls),
            Day12.create_node((1, 0), height_map_ls)
        ]
        self.assertEqual(
            {x.coord for x in child_nodes},
            {x.coord for x in Day12.check_children(curr_node, {}, height_map_ls)}
        )


class TestProccessNode(unittest.TestCase):
    def test_process_node(self):
        with open("Day12_test_input.txt") as input_file:
            raw_data = input_file.read()
        height_map_ls = [[*row] for row in raw_data.split('\n')]
        curr_node = Day12.create_node(
            (0, 0),
            height_map_ls
        )
        self.assertEqual(
            [
                ((0, 1), (((0, 0), 'a'), ((0, 1), 'a'))),
                ((1, 0), (((0, 0), 'a'), ((1, 0), 'a')))
            ],

            [
                (x[0].coord, tuple(x[1])) for x in
                Day12.process_node([(curr_node, [((0, 0), 'a')])], set(), height_map_ls, 40)[0]
            ]
        )


class TestMinStepsPathFinder(unittest.TestCase):
    def test_min_steps_path_finder(self):
        with open("Day12_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            31,
            Day12.min_steps_path_finder(raw_data)
        )


class TestMinStepsPathFinderMultipleStart(unittest.TestCase):
    def test_min_steps_path_finder_multiple_start(self):
        with open("Day12_test_input.txt") as input_file:
            raw_data = input_file.read()
        self.assertEqual(
            29,
            Day12.min_steps_path_finder_multiple_start(raw_data)
        )

if __name__ == '__main__':
    unittest.main()
