import uuid
import json
import redis
import time


class RedisQueue:
    def __init__(self, redis_url="redis://localhost:6379/0"):
        self.redis = redis.from_url(redis_url, decode_responses=True)

        # Redis keys
        self.queue_key = "queue:tasks"
        self.task_key_prefix = "task:"

    def create_task(self, task_type, payload):
        """
        Create task metadata and enqueue task ID.
        """
        task_id = str(uuid.uuid4())
        now = int(time.time())

        task_data = {
            "task_id": task_id,
            "task_type": task_type,
            "status": "pending",
            "payload": json.dumps(payload),
            "created_at": now,
            "started_at": "",
            "finished_at": "",
            "result": "",
            "error": ""
        }

        # Store task metadata
        self.redis.hset(
            f"{self.task_key_prefix}{task_id}",
            mapping=task_data
        )

        # Push task ID to queue
        self.redis.rpush(self.queue_key, task_id)

        return task_id

    def fetch_task(self, timeout=5):
        """
        Blocking pop from the queue.
        Returns task_id or None.
        """
        result = self.redis.brpop(self.queue_key, timeout=timeout)

        if result is None:
            return None

        _, task_id = result
        return task_id

    def get_task(self, task_id):
        """
        Fetch task metadata.
        """
        data = self.redis.hgetall(
            f"{self.task_key_prefix}{task_id}"
        )

        if not data:
            return None

        # Decode payload back to dict
        if data.get("payload"):
            data["payload"] = json.loads(data["payload"])

        return data
    
    def mark_running(self, task_id):
        now = int(time.time())
        self.redis.hset(
            f"{self.task_key_prefix}{task_id}",
            mapping={
                "status": "running",
                "started_at": now,
            }
        )

    def mark_success(self, task_id, result):
        now = int(time.time())
        self.redis.hset(
            f"{self.task_key_prefix}{task_id}",
            mapping={
                "status": "success",
                "result": str(result),
                "finished_at": now,
            }
        )

    def mark_failed(self, task_id, error):
        now = int(time.time())
        self.redis.hset(
            f"{self.task_key_prefix}{task_id}",
            mapping={
                "status": "failed",
                "error": str(error),
                "finished_at": now,
            }
        )
