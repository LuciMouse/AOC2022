import unittest
import Day17


class TestMakeJetPatternGenerator(unittest.TestCase):
    def test_make_jet_pattern_generator(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()
        jet_pattern_gen = Day17.make_jet_pattern_generator(raw_input)
        # this is an infinite generator, so test just past the repeat point 43
        i = 0
        output_str = ""
        while i < 43:
            output_str += next(jet_pattern_gen)
            i += 1
        self.assertEqual(
            ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>>>>",
            output_str
        )


class TestMakeRockGenerator(unittest.TestCase):
    def test_make_rock_generator(self):
        rock_gen = Day17.make_rock_generator()

        i = 0
        output_str = ""
        while i < 12:
            output_str += next(rock_gen).name
            i += 1
        self.assertEqual(
            "-+LI.-+LI.-+",
            output_str
        )


class TestDrawChamber(unittest.TestCase):
    def test_draw_chamber(self):
        curr_rock = Day17.FallingRock(
            '-',
            {
                (2, 3),
                (3, 3),
                (4, 3),
                (5, 3),
            }
        )
        top_layer = {(x, -1) for x in range(7)}  # points that form the "path" of blocking rock
        chamber_ls = Day17.draw_chamber(curr_rock, top_layer)
        for row in chamber_ls:
            print(row)
        self.assertEqual(
            [
                '..@@@@.',
                '.......',
                '.......',
                '.......',
                '-------',

            ],
            chamber_ls
        )


class TestModelFallingRocks(unittest.TestCase):
    def test_model_falling_rocks(self):
        with open("Day17_test_input.txt") as input_file:
            raw_input = input_file.read()

        self.assertEqual(
            3068,
            Day17.model_falling_rocks(raw_input, 2022)
        )


if __name__ == '__main__':
    unittest.main()