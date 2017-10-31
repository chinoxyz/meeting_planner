import unittest

import dateutil

from script import is_office_time, parse_office_hours, segments_intersection, string_to_minutes


class ScriptTest(unittest.TestCase):
    def test_string_to_minutes(self):
        self.assertEqual(string_to_minutes("0900"), 9 * 60)
        self.assertEqual(string_to_minutes("0914"), 9 * 60 + 14)

    def test_parse_office_hours(self):
        self.assertEqual(parse_office_hours("0900 1000"), (9 * 60, 10 * 60))

    # TODO: test_parse_meeting_line

    # TODO: test_parse_request_line

    def test_is_office_time(self):
        self.assertTrue(is_office_time(string_to_minutes("0900"), string_to_minutes("1000"),
                                       dateutil.parser.parse("2017/01/01 09"), dateutil.parser.parse("2017/01/01 10")))
        self.assertFalse(is_office_time(
            string_to_minutes("0900"), string_to_minutes("1000"),
            dateutil.parser.parse("2017/01/01 09:00"), dateutil.parser.parse("2017/01/01 10:01")
        ))
        self.assertFalse(is_office_time(
            string_to_minutes("0900"), string_to_minutes("1000"),
            dateutil.parser.parse("2017/01/01 08:59"), dateutil.parser.parse("2017/01/01 10:00")
        ))

    # TODO: test_parse_and_read

    # TODO: test_is_meeting_valid

    # TODO: test_create_date_dict

    # TODO: process_requests_per_day

    def test_segment_intersection(self):
        self.assertFalse(segments_intersection(1, 2, 2, 4))  # No Intersection
        self.assertFalse(segments_intersection(2, 4, 1, 2))

        self.assertTrue(segments_intersection(1, 3, 2, 4))  # One side intersection
        self.assertTrue(segments_intersection(2, 4, 1, 3))

        self.assertTrue(segments_intersection(1, 10, 2, 4))  # Containing
        self.assertTrue(segments_intersection(2, 4, 1, 10))
