"""
NO.7 Retry Mechanism Decorator: Implement a decorator to retry a function.
Develop a retry decorator that retries a function up to a specified number of times if it raises an exception.

"""



import time

def retry(attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Retrying due to error: {e}")
                    time.sleep(1)
            return None
        return wrapper
    return decorator

@retry(3)
def might_fail():
    raise ValueError("Oops!")



if __name__ == "__main__" :
        might_fail()
