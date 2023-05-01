import logging

FMT = "[{levelname:^9}] {name}: {message}"

FORMATS = {
    logging.DEBUG: f"\33[93m{FMT}\33[0m",
    logging.INFO: f"\33[32m{FMT}\33[0m",
    logging.WARNING: f"\33[33m{FMT}\33[0m",
    logging.ERROR: f"\33[31m{FMT}\33[0m",
    logging.CRITICAL: "\33[35m{message}\33[0m",
}

class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt, style="{")
        return formatter.format(record)
    


