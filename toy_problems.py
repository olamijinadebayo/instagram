def is_prime(num):
    for digit in range(1, num**0.5):
        if not num % digit == 0:
            return False
    return True
