import logging
import snap7
import random
import time

FORMAT = "%(asctime)-15s %(levelname)-8s %(message)s"
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

def Area_convert(area):
    area = area.upper()
    if area == "DB":
        return snap7.Area.DB
    elif area == "PA":
        return snap7.Area.PA
    elif area == "PE":
        return snap7.Area.CT
    elif area == "TM":
        return snap7.Area.TM
    elif area == "MK":
        return snap7.Area.PE
    elif area == "CT":
        return snap7.Area.CT
    else:
        raise ValueError(f"Invalid area: {area}")

def read_area(client, area, db_number, start, size):
    """
    Read data from a specified area in the PLC.
    
    Args:
        client (snap7.client.Client): The Snap7 client object.
        area (int): The area to read from (e.g., snap7.types.S7AreaDB).
        db_number (int): The DB number (only relevant for DB area).
        start (int): The starting address to read from.
        size (int): The number of bytes to read.
    
    Returns:
        bytes: The data read from the PLC.
    """
    if Area_convert(area) == snap7.Area.DB:
        return client.db_read(db_number, start, size)
    else:
        return client.read_area(area, db_number, start, size)




def write_area(client, area, db_number, start, data):
    """
    Write data to a specified area in the PLC.
    
    Args:
        client (snap7.client.Client): The Snap7 client object.
        area (int): The area to write to (e.g., snap7.types.S7AreaDB).
        db_number (int): The DB number (only relevant for DB area).
        start (int): The starting address to write to.
        data (bytes): The data to write to the PLC.
    
    Returns:
        bool: True if the write was successful, False otherwise.
    """
    if isinstance(data, int):
        old_data = data
        data = bytearray(1)
        data[0] = old_data
    if Area_convert(area) == snap7.Area.DB:
        return client.db_write(db_number, start, bytearray(data))
    return client.write_area(area, db_number, start, data)




def fuzz_area(client, area, db_number, start, size,safe=False, limit=10):
    """
    Fuzz data in a specified area in the PLC.
    
    Args:
        client (snap7.client.Client): The Snap7 client object.
        area (int): The area to fuzz (e.g., snap7.types.S7AreaDB).
        db_number (int): The DB number (only relevant for DB area).
        start (int): The starting address to fuzz.
        size (int): The number of bytes to fuzz.
    """
    # Generate random data to fuzz
    fuzz_data = bytearray(size)
    for i in range(size):
        fuzz_data[i] = random.randint(0, limit - 1)
    if safe:
        log.info("Safe mode enabled. Restoring original data after fuzzing.")
        # Get the current data to avoid overwriting important values
        current_data = read_area(client, area, db_number, start, size)
        log.info(f"Current data before fuzzing: {current_data}")

    # Write the fuzz data to the PLC
    write_area(client, area, db_number, start, fuzz_data)

    if safe:
        # Restore the original data after fuzzing
        write_area(client, area, db_number, start, current_data)
    
    # Read back the data to verify the fuzzing
    read_data = read_area(client, area, db_number, start, size)
    
    # Log the fuzzed data
    logging.info(f"Fuzzed data: {fuzz_data}")
    logging.info(f"Read back data: {read_data}")

def gather_info(client):
    """
    Gather information from the PLC.
    
    Args:
        client (snap7.client.Client): The Snap7 client object.
    
    Returns:
        dict: A dictionary containing gathered information.
    """
    try:
        order_code = client.get_order_code()
    except:
        order_code = "Unknown"
    log.info(f"Order Code: {order_code}")
    try:
        version = client.get_version()
    except:
        version = "Unknown"
    log.info(f"Version: {version}")
    try:
        cpu_info = client.get_cpu_info()
    except:
        cpu_info = "Unknown"
    log.info(f"Module Name: {cpu_info.ModuleName}")
    log.info(f"Serial Number: {cpu_info.SerialNumber}")
    log.info(f"Module AS Name: {cpu_info.ASName}")
    log.info(f"Module Copy Right: {cpu_info.Copyright}")

    try:
        cpu_state = client.get_cpu_state()
    except:
        cpu_state = "Unknown"
    log.info(f"CPU State: {cpu_state}")


def fuzz_train(client, area, db_number, start,end, wait):
    """
    Fuzz training data in a specified area in the PLC.
    
    Args:
        client (snap7.client.Client): The Snap7 client object.
        area (int): The area to fuzz (e.g., snap7.types.S7AreaDB).
        db_number (int): The DB number (only relevant for DB area).
        start (int): The starting
        size (int): The number of bytes to fuzz.
    """
    log.info("[*] Fuzz data")
    for i in range(start, end):
        data = client.db_read(db_number, i, 1)
        if data == bytearray(b'\x00'):
            new_data = bytearray(b'\x02')
        elif data == bytearray(b'\x01'):
            new_data = bytearray(b'\x00')
        elif data == bytearray(b'\x02'):
            new_data = bytearray(b'\x00')
        else:
            new_data = data
        client.db_write(db_number, i, new_data)
        log.info(f"Fuzzed address {i} with data {new_data}")
        time.sleep(wait)



