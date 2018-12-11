from celery import Celery

app = Celery('tasks', broker='amqp://guest@tiny_rabbitmq//', backend='amqp')

@app.task()
def add(x, y): return x + y

@app.task()
def tsum(numbers):
    numbers = list(numbers)
    n = len(numbers)
    a = str(numbers[0]) if n > 0 else ' '
    return sum(numbers)

if __name__ == '__main__':
    app.worker_main()
