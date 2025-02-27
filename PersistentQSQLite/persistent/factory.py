from persistent.persistent_map import Persistent_blueprint

def get_queue(backend: str = "sqlite") :
    """
    Factory method to get an instance of a persistent queue implementation.
    """
    if backend.lower() == "sqlite":
        from .persistent_queue import PersistentQSQLite
        return PersistentQSQLite()
    # Future implementations can be added here.
    # elif backend.lower() == "postgres":
    #     from persistentq.persistentq_postgres import PersistentQPostgres
    #     return PersistentQPostgres()
    else:
        raise ValueError(f"Unsupported backend: {backend}")
