def coroutine(func):
    def send_next(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr
    return send_next


@coroutine
def my_coroutine():
    try:
        while True:
            i = 10 * (yield)
            print(i)
    except GeneratorExit:
        print("goodbye")


mc = my_coroutine()
for i in range(17):
    mc.send(i)

mc.close()
