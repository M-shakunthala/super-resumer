from core.config import Config


class JobRanker:

    def __init__(self):
        self.config = Config.load()
        self.ranking_config = self.config.get('ranking', {})
        self.min_score = self.ranking_config.get('min_score_threshold', 0.5)
        self.max_jobs = self.ranking_config.get('max_ranked_jobs', 20)

    def rank(self, jobs):

        # Filter jobs below minimum score
        qualified = [
            job for job in jobs
            if job.get("score", 0) >= self.min_score
        ]

        # Sort by score (descending)
        ranked = sorted(
            qualified,
            key=lambda x: (
                x.get("score", 0)
            ),
            reverse=True
        )

        # Limit to max jobs
        return ranked[:self.max_jobs]
