import time
from task_queue.redis_queue import RedisQueue


def execute_task(task):
    """
    Dummy task execution logic.
    Replace this later with real task handlers.
    """
    print(f"Executing task {task['task_id']} with payload {task['payload']}")
    time.sleep(2)  # simulate work
    return {"message": "Task completed successfully"}


def start_worker():
    queue = RedisQueue()
    print("Worker started. Waiting for tasks...")

    while True:
        task_id = queue.fetch_task()

        if task_id is None:
            continue

        task = queue.get_task(task_id)

        try:
            queue.mark_running(task_id)

            result = execute_task(task)

            queue.mark_success(task_id, result)
            print(f"Task {task_id} completed")

        except Exception as e:
            queue.mark_failed(task_id, str(e))
            print(f"Task {task_id} failed: {e}")


if __name__ == "__main__":
    start_worker()
