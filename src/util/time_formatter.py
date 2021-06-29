from datetime import timedelta


class TimeFormatter:
    HOURS = 0
    MINUTES = 1
    SECONDS = 2
    MS = 3
    US = 4

    def __init__(self, time, time_format):
        self._time = time
        self._format = time_format

    def _ms(self):
        return self._time

    def _s_ms(self):
        time = self._format_timings(split_at=self.SECONDS)
        return time

    def _m_s(self):
        time = self._format_timings(split_at=self.MINUTES)
        time_no_ms = time.split('.')[0]
        return time_no_ms

    def _m_s_ms(self):
        time = self._format_timings(split_at=self.MINUTES)
        return time

    def str(self):
        # return str(self._get_format(self._format)())
        return self._get_format(self._format)()

    def _format_timings(self, split_at):
        us_time = timedelta(microseconds=self._time)

        splitted_time = str(us_time).split(':')[split_at:]

        join_back = ':'.join(splitted_time)

        return join_back

    def _get_format(self, time_format):
        time_format = time_format.replace('_', ':')
        formats = {
            'ms': self._ms,
            's:ms': self._s_ms,
            'm:s': self._m_s,
            'm:s:ms': self._m_s_ms
        }
        return formats[time_format]
