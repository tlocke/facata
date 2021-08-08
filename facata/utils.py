from contextlib import AbstractContextManager


class PreparedStatement(AbstractContextManager):
    def __init__(self, ps):
        self.ps = ps

    def run(self, **params):
        return self.ps.run(**params)

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.ps.close()


class Connection(AbstractContextManager):
    def __init__(self, con, module=None):
        self.con = con
        self.cur = con.cursor()
        self.module = module

    def run(self, sql, **params):
        self.cur.execute(sql, params)
        return self.cur.fetchall()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self.cur.close()
        self.con.close()

    def register_py_to_db(self, cls, type_code, adapter):
        pass

    def register_db_to_py(self, type_code, adapter):
        pass

    def prepare(self, sql):
        class Ps:
            def __init__(self, con, sql):
                self.con = con
                self.sql = sql

            def run(self, **params):
                return self.con.run(sql, **params)

            def close(self):
                pass

        return Ps(self, sql)

    @property
    def columns(self):
        description = self.cur.description
        if description is None:
            return None
        else:
            cols = []
            # column name, type_code, display_size, internal_size, precision,
            # scale, null_ok
            for col in description:
                cols.append(
                    dict(
                        zip(
                            (
                                "name",
                                "type_code",
                                "display_size",
                                "internal_size",
                                "precision",
                                "scale",
                            ),
                            col,
                        )
                    )
                )
            return cols

    @property
    def connection(self):
        return self.con


OUTSIDE = 0  # outside quoted string
INSIDE_SQ = 1  # inside single-quote string '...'
INSIDE_QI = 2  # inside quoted identifier   "..."
INSIDE_ES = 3  # inside escaped single-quote string, E'...'
INSIDE_PN = 4  # inside parameter name eg. :name
INSIDE_CO = 5  # inside inline comment eg. --


def to_pyformat(sql):
    in_quote_escape = False
    placeholder = []
    output_query = []
    state = OUTSIDE
    prev_c = None

    for i, c in enumerate(sql):
        next_c = sql[i + 1] if i + 1 < len(sql) else None

        if state == OUTSIDE:
            if c == "'":
                output_query.append(c)
                if prev_c == "E":
                    state = INSIDE_ES
                else:
                    state = INSIDE_SQ
            elif c == '"':
                output_query.append(c)
                state = INSIDE_QI
            elif c == "-":
                output_query.append(c)
                if prev_c == "-":
                    state = INSIDE_CO
            elif c == ":" and next_c not in ":=" and prev_c != ":":
                state = INSIDE_PN
                placeholder.clear()
            else:
                output_query.append(c)

        elif state == INSIDE_SQ:
            if c == "'":
                if in_quote_escape:
                    in_quote_escape = False
                elif next_c == "'":
                    in_quote_escape = True
                else:
                    state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_QI:
            if c == '"':
                state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_ES:
            if c == "'" and prev_c != "\\":
                # check for escaped single-quote
                state = OUTSIDE
            output_query.append(c)

        elif state == INSIDE_PN:
            placeholder.append(c)
            if next_c is None or (not next_c.isalnum() and next_c != "_"):
                state = OUTSIDE
                output_query.append(f"%({''.join(placeholder)})s")

        elif state == INSIDE_CO:
            output_query.append(c)
            if c == "\n":
                state = OUTSIDE

        prev_c = c

    return "".join(output_query)
