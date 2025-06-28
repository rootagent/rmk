import datetime
import uuid


def generate_session_id():
    current_datetime = datetime.datetime.now()
    date_string = current_datetime.strftime("%Y%m%d%H%M%S")
    # Generate a random UUID and convert to hex string
    unique_identifier = uuid.uuid4().hex
    session_id = f"{date_string}-{unique_identifier}"
    return session_id
