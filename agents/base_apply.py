from abc import ABC, abstractmethod


class BaseApply(ABC):

    @abstractmethod
    def apply(
        self,
        job_url,
        resume_path
    ):
        pass
