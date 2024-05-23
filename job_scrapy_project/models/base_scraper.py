from abc import ABC, abstractmethod

class BaseScraper(ABC):
    # 文件输出路径
    OUTPUT_PATH = "data/output/"

    @abstractmethod
    def get_job_description(self, job_id):
        pass

    @abstractmethod
    def get_recommended_candidates(self, job_id):
        pass

    @abstractmethod
    def get_candidate_details(self, candidate):
        pass

    @abstractmethod
    def filter_candidates(self, job_description, candidates):
        pass

    @abstractmethod
    def compare_with_job(self, job_description, candidate_details):
        pass

    @abstractmethod
    def greet_candidate(self, candidate_contact):
        pass