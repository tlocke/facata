def connect(dbname, username, password, host, port, params):
    import pg8000.native

    for param, paramname in ((host, "host"), (port, "port")):
        if param is not None:
            params[paramname] = param

    return pg8000.native.Connection(
        username, database=dbname, password=password, **params
    )
