from typedobject import Object

a = Object(a = 1)

def test_simple_keyword_assignment() -> None:
    assert a.a + 0 == 1 
    b = Object(a = 1, b = 2)
    assert b.b + 0 == 2 

def test_nested_keyword_assignment() -> None:
    b = Object(b = a)
    assert b.b.a + 0 == 1

    c = Object(c = b)
    assert c.c.b.a + 0 == 1

def test_simple_copy() -> None:
    c = Object(a)
    assert c.a + 0 == 1

def test_overwrite_by_copy() -> None:
    res = Object(Object(a = 1), Object(a = '2'), Object(a = None))
    assert res.a is None 
  
def test_overwrite_by_keyword() -> None:
    res = Object(Object(a = 1, b = 2), a = '1')
    assert res.a + '' == '1'