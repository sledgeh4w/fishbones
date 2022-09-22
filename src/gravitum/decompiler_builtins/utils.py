from ..utils import get_type


def truncate(x, c, to_type):
    """Truncate data."""
    data = x.to_bytes()
    to_size = to_type.get_size()
    return to_type.from_bytes(data[c : c + to_size])


def zero_extend(x, to_type):
    """Zero extend."""
    return to_type.from_bytes(x.to_bytes())


def sign_extend(x, to_type):
    """Sign extend."""
    t1 = get_type(size=x.get_size(), signed=True)
    t2 = get_type(size=to_type.get_size(), signed=True)
    return to_type.from_bytes(t2.from_bytes(t1(x).to_bytes()).to_bytes())
