import datetime
import sys

import dateutil.parser


def string_to_minutes(time_str):
    # Assume the string is in correct format
    return int(time_str[0:2]) * 60 + int(time_str[2:])


def parse_office_hours(line):
    start, end = map(string_to_minutes, line.strip().split(' '))
    assert (start <= end)
    return start, end


def parse_meeting_line(line):
    meeting_time_str, duration_str = line.strip().rsplit(' ', 1)
    duration = int(duration_str)
    assert (0 < duration and duration < 24)
    return dateutil.parser.parse(meeting_time_str), int(duration)


def parse_request_line(line):
    request_time_str, employee_id = line.strip().rsplit(' ', 1)
    return dateutil.parser.parse(request_time_str), employee_id


def is_office_time(office_start_minute, office_end_minute, meeting_time, meeting_end):
    assert (meeting_time.date() == meeting_end.date())
    start_datetime = datetime.datetime.combine(meeting_time.date(), datetime.time.min) + datetime.timedelta(
        minutes=office_start_minute)
    end_datetime = datetime.datetime.combine(meeting_time.date(), datetime.time.min) + datetime.timedelta(
        minutes=office_end_minute)

    return start_datetime <= meeting_time and end_datetime >= meeting_end


def parse_and_read():
    office_start_minute, office_end_minute = parse_office_hours(sys.stdin.readline())

    request_list = []
    for request_line in sys.stdin:
        meeting_line = next(sys.stdin)
        request_time, employee_id = parse_request_line(request_line)
        meeting_time, duration_hours = parse_meeting_line(meeting_line)
        meeting_end = meeting_time + datetime.timedelta(hours=duration_hours)
        if (not is_office_time(office_start_minute, office_end_minute, meeting_time, meeting_end)):
            continue

        request_list.append(
            (request_time, employee_id, meeting_time, meeting_end)
        )

    return request_list


def segments_intersection(start_s1, end_s1, start_s2, end_s2):
    assert (start_s1 < end_s1)
    assert (start_s2 < end_s2)
    min_end = min(end_s1, end_s2)
    max_start = max(start_s1, start_s2)
    return min_end > max_start


def is_meeting_valid(plan, current_meeting_time, current_meeting_end):
    for meeting_time, meeting_end, _ in plan:
        if (segments_intersection(current_meeting_time, current_meeting_end, meeting_time, meeting_end)):
            return False
    return True


def create_date_dict(request_list):
    day_events_dict = {}
    for (id, (_, _, meeting_time, _)) in enumerate(request_list):
        meeting_date = meeting_time.date()
        if meeting_date not in day_events_dict:
            day_events_dict[meeting_date] = []
        day_events_dict[meeting_date].append(id)
    return day_events_dict


def process_requests_per_day(request_list, day_events_dict):
    result = []
    for date, id_list in (day_events_dict.items()):

        date_sorted_requests = sorted([request_list[id] for id in id_list])
        date_plan = []

        for _, employee_id, current_meeting_time, current_meeting_end in date_sorted_requests:
            if not is_meeting_valid(date_plan, current_meeting_time, current_meeting_end):
                break
            date_plan.append((current_meeting_time, current_meeting_end, employee_id))
        result.append((date, sorted(date_plan)))
    return result


def print_result(result):
    for date, plan in sorted(result):
        print(date)
        for meeting_time, meeting_end, employee_id in plan:
            print('%02d:%02d %02d:%02d %s' % (
                meeting_time.hour, meeting_time.minute,
                meeting_end.hour, meeting_end.minute,
                employee_id)
                  )


if __name__ == '__main__':
    request_list = parse_and_read()

    day_events_dict = create_date_dict(request_list)

    result = process_requests_per_day(request_list, day_events_dict)

    print_result(result)
