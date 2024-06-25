# utils.py

from datetime import datetime,timedelta

class DateValidationUtility:
    DATE_FORMAT = "%Y-%m-%d"
    SUPPORTED_FORMATS = ["%m/%d/%Y",]

    @classmethod
    def parse_date(cls, date_str):
        for fmt in cls.SUPPORTED_FORMATS:
            try:
                return datetime.strptime(date_str, fmt).strftime(cls.DATE_FORMAT)
            except ValueError:
                continue
        return None

    @classmethod
    def validate_dates(cls, start_date, end_date):
        errors = []
        parsed_start_date = cls.parse_date(start_date) if start_date else None
        parsed_end_date = cls.parse_date(end_date) if end_date else None
        
        supported_formats_msg = ", ".join(cls.SUPPORTED_FORMATS)
        
        if start_date and not parsed_start_date:
            errors.append(f"Invalid start_date '{start_date}'. Expected formats are: {supported_formats_msg}.")
        if end_date and not parsed_end_date:
            errors.append(f"Invalid end_date '{end_date}'. Expected formats are: {supported_formats_msg}.")
        
        if (parsed_start_date and not parsed_end_date) or (parsed_end_date and not parsed_start_date):
            errors.append("Both start_date and end_date must be provided")
        
        if parsed_start_date and parsed_end_date and parsed_end_date < parsed_start_date:
            errors.append("end_date must be greater than or equal to start_date.")
        
        return parsed_start_date, parsed_end_date, errors


def get_formatted_due_date(due_date):
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        
        if due_date.date() == now.date():
            return due_date.strftime("%I:%M %p")  # Return time alone if due today
        elif due_date.date() == tomorrow.date():
            return "Tomorrow"  # Return "Tomorrow" if due tomorrow
        else:
            return due_date.strftime("%Y/%m/%d")  # Return full date for other days