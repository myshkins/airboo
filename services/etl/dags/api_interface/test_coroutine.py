
def next_cr(func):
    def call_next(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.next()
    return call_next


# @next_cr
def my_coroutine(n: int):
    i = 2 + (yield)
    print(i)


i = 3
breakpoint()
x = my_coroutine(i)
x.send(None)
for i in range(3):
    x.send(i * 2)
