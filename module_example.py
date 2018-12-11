from celery import chord, chain
from tasks import add, tsum

def test_celery_chain(N = 100):
    def _generate_test_chain(n):
        gt_result = n * (1 + n) / 2

        first = add.s(0, 0)
        body = [add.s(i + 1) for i in range(N)]
        c = chain(first, *body)
        return c, gt_result

    task, result = _generate_test_chain(N)
    return task.apply_async()
    
def test_celery_chord_multiple(N = 1):
    def _generate_test_chord(n):
        gt_result = n
        task = add.si(1, 0)

        def _generate_chord_inner(n):
            if n <= 0:
                return tsum.s()
            else:
                return chord(header=[tsum.s(), task.clone()], body=_generate_chord_inner(n - 1))
        return chord(header=add.s(0, 1), body=_generate_chord_inner(n - 1)), gt_result

    my_chord, result_gt = _generate_test_chord(N)
    return my_chord.apply_async()
