def get_gzip_uncompressed_file_size(file_name):
    """
    this function will return the uncompressed size of a gzip file
    similar as gzip -l file_name
    """
    file_obj = gzip.open(file_name, 'r')
    file_obj.seek(-8, 2)
    crc32 = gzip.read32(file_obj)
    isize = gzip.read32(file_obj)
    return isize
