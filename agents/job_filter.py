from core.config import Config


class JobFilter:

    def __init__(self):
        self.config = Config.load()
        self.blacklist = self.config.get('title_blacklist', [
            "senior",
            "lead", 
            "architect",
            "manager"
        ])

    def is_valid(
        self,
        job,
        profile_skills
    ):

        title = (
            job["title"].lower()
        )

        for word in self.blacklist:
            if word in title:
                return False

        return True
