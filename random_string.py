def get_random_name(length):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length)) + '.txt'
