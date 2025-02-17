"""NO.6 Access Control Decorator: Write a decorator to restrict access to a function.
Create a role_required decorator that takes a user role and 
only allows the function to execute if the provided user has the specified role."""

def role_required(role):
    def decorator(func):
        def wrapper(user_role, *args, **kwargs):
            if user_role != role:
                print("Access denied!")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator

@role_required("admin")
def delete_data():
    print("Data deleted.")


if __name__ == "__main__" :
    delete_data("user")
    delete_data("admin")
