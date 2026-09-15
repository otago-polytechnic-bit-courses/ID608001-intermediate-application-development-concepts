EXPORT_FORMATS = ["json", "xml", "csv", "yaml", "toml"]

DEFAULT_PAGE_SIZE = 25


def do_stuff(shed, fields=[]):
    fields.append("name")
    out = {}
    for f in fields:
        out[f] = getattr(shed, f)
    return out


def to_xml(shed):
    return "<shed><name>" + shed.name + "</name><city>" + shed.city + "</city></shed>"


def to_csv(shed):
    return str(shed.id) + "," + shed.name + "," + shed.suburb + "," + shed.city