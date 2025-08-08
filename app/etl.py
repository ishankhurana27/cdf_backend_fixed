from datetime import datetime, timedelta
import json
import logging
import math
import uuid
import pandas as pd
from io import BytesIO
from pathlib import Path


import pandas as pd



def convert_to_cdf(json_data: dict,upload_uuid: str,file_uuid: str) -> dict:
    ts = json_data.get("struct_update_track_timestamp", {})

    msg_date = f"{ts.get('date_dd', '00').zfill(2)}-{ts.get('date_mm', '00').zfill(2)}-{ts.get('date_yy', '0000')}"
    msg_time = f"{ts.get('time_hour', '00').zfill(2)}:{ts.get('time_minute', '00').zfill(2)}:{ts.get('time_second', '00')}"

    try:
        timestamp_str = convert_to_postgres_timestamp(msg_date, msg_time)
        timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
    except ValueError as e:
        logging.warning(f"Skipping line: Invalid date format: {msg_date}")
        return None

    return {
        "latitude": float(json_data["latitude"]),
        "longitude": float(json_data["longitude"]),
        "speed": float(json_data["speed"]),
        "bearing": float(json_data["bearing"]),
        "course": float(json_data["course"]),
        "logged_timestamp": timestamp,
        "sys_trk_no": int(json_data["sys_trk_no"]),
        "location": f'POINT({json_data["longitude"]} {json_data["latitude"]})',
        "raw_data": json_data,
        "uuid": upload_uuid,
        "file_uuid": file_uuid,

    }

def convert_to_p8i(row, record_uuid):
    return {
        "uuid": record_uuid,
        "affiliation": row.get("Affiliation", None),
        "change_type": row.get("Change Type", None),
        "environment": row.get("Environment", None),
        "platform_name": row.get("Platform Name", None),
        "platform_type": row.get("Platform Type", None),
        "trk_short_name": row.get("Trk Short Name", None),
        "trk_display_num": row.get("Trk Display Num", None),
        "lat_lat_origin": row.get("Lat / Lat Origin", None),
        "position_bearing": row.get("Position/Bearing", None),
        "msg_date": row.get("Msg Date YYYYMMDD", None),
        "speed_kts": row.get("Speed Kts / Spare", None),
        "long_long_origin": row.get("Long / Long Origin", None),
        "platform_spec_type": row.get("Platform Spec Type", None),
        "target_of_interest": row.get("Target of Interest", None),
        "altitude_feet": row.get("Altitude Feet / Spare", None),
        "msg_time": row.get("Msg Time hh:mm:ss.sss", None),
        "course_deg": row.get("Course Deg / Bearing Deg", None),
        "position_valid_date": row.get("Position Valid Date YYYYMMDD", None),
        "position_valid_time": row.get("Position Valid Time hh:mm:ss.sss", None)
    }


def convert_to_cdf_from_csv_row(row: dict,upload_uuid: str) -> dict:
    timestamp = convert_to_postgres_timestamp(row["Position Valid Date YYYYMMDD"], row["Position Valid Time hh:mm:ss.sss"])
    return {
        "latitude": dms_to_decimal(row["Lat / Lat Origin"]),
        "longitude": dms_to_decimal(row["Long / Long Origin"]),
        "speed": float(row["Speed Kts / Spare"]),
        "bearing": float(row.get("Course Deg / Bearing Deg", 0)),
        "course": float(row.get("Course Deg / Bearing Deg", 0)),
        "logged_timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f"),
        "raw_data": dict(row),
        "uuid": upload_uuid
    }
def convert_to_piracy(row: dict, upload_uuid: str) -> dict:
  
    timestamp = convert_to_postgres_timestamp(
        row["date"],
        row["time"]
    )
    
    return {
        "latitude": row["latitude"],
        "longitude": row["longitude"],
        "logged_timestamp": datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f"),
        "raw_data": json.dumps(clean_nan(row.to_dict())),
        "uuid": upload_uuid,
        "vessel_name": str(row.get("vessel_name", "")).strip()
    }


def clean_nan(obj):
    """
    Recursively convert float('nan') → None for dicts/lists
    """
    if isinstance(obj, dict):
        return {k: clean_nan(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_nan(v) for v in obj]
    elif isinstance(obj, float) and math.isnan(obj):
        return None
    else:
        return obj

# def convert_to_piracy(row: dict,upload_uuid: str) -> dict:
#     latitude = float(row["latitude"])
#     longitude = float(row["longitude"])
#     return {
#         "location": f'POINT({longitude} {latitude})',
#         "datetime": f"{row.get('date', '').strip()} {row.get('time', '').strip()}",
#         "attack_description": row.get("attack_description", "").strip(),
#         "vessel_name": row.get("vessel_name", "").strip(),
#         "vessel_type": row.get("vessel_type", "").strip(),
#         "vessel_status": row.get("vessel_status", "").strip(),
#         "timestamp": row.get("Timestamp", "").strip(),
#         "raw_data": dict(row),
#         "uuid": upload_uuid
#     }

# def convert_to_ais(row: dict,upload_uuid: str) -> dict:
#     return {
#         "timestamp": row.get("Timestamp", row.get("BaseDateTime", "")).strip(),
#         "vessel_name": row.get("VesselName", "").strip(),
#         "imo": row.get("IMO", "").strip(),
#         "raw_data": dict(row),
#         "uuid": upload_uuid,
#         "mmsi": row.get("MMSI", "").strip(),
#         "latitude": dms_to_decimal(row["Lat / Lat Origin"]),
#         "longitude": dms_to_decimal(row["Lon / Lon Origin"]),
#         "speed": float(row["SOG / Spare"]), #Speed Kts
#         "course": float(row.get("COG / Bearing Deg", 0)), #Course Deg 
#     }

def convert_to_ais(row: dict, upload_uuid: str) -> dict:
    return {
        "logged_timestamp": str(row.get("Timestamp", row.get("BaseDateTime", ""))).strip(),
        "vessel_name": str(row.get("VesselName", "")).strip(),
        "imo": str(row.get("IMO", "")).strip(),
        "mmsi": str(row.get("MMSI", "")).strip(),
        "latitude":(row.get("LAT")),
        "longitude":(row.get("LON")),
        "speed": float(row.get("SOG")),
        "course": float(row.get("Heading")),
        "raw_data": json.dumps(clean_nan(row.to_dict())),
        "uuid": upload_uuid
    }




# def convert_to_postgres_timestamp(msg_date: str, msg_time: str) -> str:
    
#     print(msg_date,msg_time)
#     msg_date = str(msg_date)
#     msg_time=str(msg_time)
#     print(type(msg_date),type(msg_time))
#     date_obj = datetime.strptime(msg_date, "%Y%m%d").date()

#     parts = msg_time.split(":")
#     if len(parts) == 2:
#         hours = 0
#         minutes = int(parts[0])
#         seconds = float(parts[1])
#     elif len(parts) == 3:
#         hours = int(parts[0])
#         minutes = int(parts[1])
#         seconds = float(parts[2])
#     else:
#         raise ValueError(f"Invalid time format: {msg_time}")

#     secs_int = int(seconds)
#     micros = int((seconds - secs_int) * 1_000_000)
#     time_delta = timedelta(
#         hours=hours,
#         minutes=minutes,
#         seconds=secs_int,
#         microseconds=micros
#     )

#     full_dt = datetime.combine(date_obj, datetime.min.time()) + time_delta

#     return full_dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
def convert_to_postgres_timestamp(msg_date: str, msg_time: str) -> str:
    from datetime import datetime, timedelta

    msg_date = str(msg_date).strip().split(".")[0]
    msg_time = str(msg_time).strip().upper()

    try:
        if "-" in msg_date:
            date_obj = datetime.strptime(msg_date, "%d-%m-%Y").date()
        elif len(msg_date) == 8 and msg_date.isdigit():
            date_obj = datetime.strptime(msg_date, "%Y%m%d").date()
        else:
            raise ValueError
    except ValueError as e:
        raise ValueError(f"Invalid date format: {msg_date}") from e

    if not msg_time or msg_time in {"NA", "NAN"}:
        minutes = 0
        seconds = 0
        time_delta = timedelta(minutes=minutes, seconds=seconds)
    else:
        msg_time = msg_time.replace("UTC", "").replace("GMT", "").strip()
        if "," in msg_time:
            msg_time = msg_time.split(",")[0].strip()

        try:
            parts = msg_time.split(":")
            if len(parts) == 2:
                minutes = int(parts[0])
                seconds = float(parts[1])
            elif len(parts) == 3:
                # Original expected format
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                secs_int = int(seconds)
                micros = int((seconds - secs_int) * 1_000_000)
                time_delta = timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=secs_int,
                    microseconds=micros
                )
                full_dt = datetime.combine(date_obj, datetime.min.time()) + time_delta
                return full_dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"Invalid time format: {msg_time}")

        secs_int = int(seconds)
        micros = int((seconds - secs_int) * 1_000_000)
        time_delta = timedelta(
            minutes=minutes,
            seconds=secs_int,
            microseconds=micros
        )

    full_dt = datetime.combine(date_obj, datetime.min.time()) + time_delta
    return full_dt.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

# def parse_structured_file(file) -> pd.DataFrame:
#     filename = file.filename.lower()
#     file.file.seek(0)
#     if filename.endswith(".csv"):
#         return pd.read_csv(BytesIO(file.file.read()))
#     elif filename.endswith(".tsv"):
#         return pd.read_csv(BytesIO(file.file.read()), sep="\t")
#     elif filename.endswith(".xlsx"):
#         return pd.read_excel(BytesIO(file.file.read()))
#     else:
#         raise ValueError("Unsupported file format")

def parse_structured_file(file_bytes: bytes, filename: str) -> pd.DataFrame:
    filename = filename.lower()
    if filename.endswith(".csv"):
        return pd.read_csv(BytesIO(file_bytes))
    elif filename.endswith(".tsv"):
        return pd.read_csv(BytesIO(file_bytes), sep="\t")
    elif filename.endswith(".xlsx"):
        return pd.read_excel(BytesIO(file_bytes))
    else:
        raise ValueError("Unsupported file format")

    
def dms_to_decimal(coord_str: str) -> float:
    try:
        dms, direction = coord_str.strip().split()
        degrees, minutes, seconds = map(float, dms.split(":"))
        decimal = degrees + minutes / 60 + seconds / 3600
        if direction in ("S", "W"):
            decimal *= -1
        return round(decimal, 6)
    except Exception as e:
        raise ValueError(f"Invalid coordinate format: {coord_str}")


def convert_to_mmsi(row: dict, upload_uuid: str, file_uuid: str) -> dict:
    def parse_float(val):
        try:
            if pd.isna(val) or val == "" or val is None:
                return None
            return float(val)
        except Exception:
            return None

    def parse_int(val):
        try:
            if pd.isna(val) or val == "" or val is None:
                return None
            return int(float(val))  # Handles cases where int is given as float string
        except Exception:
            return None

    def parse_str(val):
        if pd.isna(val) or val is None:
            return ""
        return str(val)

    def parse_dt(val):
        try:
            if pd.isna(val) or val == "" or val is None:
                return None
            # Try both with and without seconds fraction
            try:
                return datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S")
            except ValueError:
                return datetime.strptime(str(val), "%Y-%m-%d %H:%M:%S.%f")
        except Exception:
            return None

    return {
        "nav_status": parse_str(row.get("nav_status")),
        "rot": parse_float(row.get("rot")),
        "sog": parse_float(row.get("sog")),
        "latitude": parse_float(row.get("latitude")),
        "longitude": parse_float(row.get("longitude")),
        "cog": parse_float(row.get("cog")),
        "true_heading": parse_int(row.get("true_heading")),
        "imo": parse_int(row.get("imo")),
        "ship_name": parse_str(row.get("ship_name")),
        "call_sign": parse_str(row.get("call_sign")),
        "ship_type": parse_str(row.get("ship_type")),
        "draught": parse_float(row.get("draught")),
        "destination": parse_str(row.get("destination")),
        "dimbow": parse_int(row.get("dimbow")),
        "dimstern": parse_int(row.get("dimstern")),
        "dimport": parse_int(row.get("dimport")),
        "dimstarboard": parse_int(row.get("dimstarboard")),
        "eta": parse_dt(row.get("eta")),
        "beam": parse_int(row.get("beam")),
        "length": parse_int(row.get("length")),
        "rec_time": parse_dt(row.get("rec_time")),
        "source": parse_str(row.get("source")),
        "country": parse_str(row.get("country")),
        "flag_name": parse_str(row.get("flag_name")),
        "file_uuid": file_uuid,
        "uuid": upload_uuid
    }


