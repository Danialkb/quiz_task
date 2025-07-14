from typing import Iterable
from uuid import UUID
from redis.asyncio import Redis

from db.models import QuizSession


class QuizStatsService:
    STATS_TTL = 604800  # 7 days

    def __init__(self, redis: Redis):
        self.redis = redis

    def get_bucket_key(self, quiz_id: UUID) -> str:
        return f"quiz_stats:{quiz_id}:buckets"

    def get_bucket_name(self, index: int) -> str:
        return f"{index}_{index + 10}"

    async def set_stats(self, quiz_id: UUID, quiz_sessions: Iterable[QuizSession]):
        bucket_key = self.get_bucket_key(quiz_id)

        bucket_counts: dict[str, int] = {
            self.get_bucket_name(i): 0 for i in range(0, 100, 10)
        }

        for session in quiz_sessions:
            score = (session.correct_answers / session.questions_count) * 100
            bucket = self.get_bucket_name(int(score // 10 * 10))
            bucket_counts[bucket] += 1

        async with self.redis.pipeline() as pipe:
            await pipe.hset(bucket_key, mapping=bucket_counts)
            await pipe.expire(bucket_key, self.STATS_TTL)
            await pipe.execute()

    async def get_user_percentile(self, quiz_id: UUID, user_score: float) -> float:
        if user_score == 0:
            return 0
        bucket_key = self.get_bucket_key(quiz_id)
        bucket_counts = await self.redis.hgetall(bucket_key)
        bucket_counts = {k.decode(): int(v.decode()) for k, v in bucket_counts.items()}

        if not bucket_counts:
            return 100

        total_people = sum(int(count) for count in bucket_counts.values())
        user_bucket = int(user_score // 10 * 10) + 10
        worse_people = 0

        for bucket in range(0, user_bucket + 10, 10):
            bucket_name = self.get_bucket_name(bucket)
            print(bucket_name)
            worse_people += int(bucket_counts.get(bucket_name, 0))

        return round((worse_people / total_people) * 100, 2)
