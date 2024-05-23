from models.base_scraper import BaseScraper

class ProxyScraper(BaseScraper):
    def __init__(self, real_scraper):
        self.real_scraper = real_scraper

    def get_job_description(self, job_id):
        return self.real_scraper.get_job_description(job_id)

    def get_recommended_candidates(self, job_id):
        return self.real_scraper.get_recommended_candidates(job_id)

    def get_candidate_details(self, candidate):
        return self.real_scraper.get_candidate_details(candidate)

    def filter_candidates(self, job_description, candidates):
        return self.real_scraper.filter_candidates(job_description, candidates)

    def compare_with_job(self, job_description, candidate_details):
        return self.real_scraper.compare_with_job(job_description, candidate_details)

    def greet_candidate(self, candidate_contact):
        return self.real_scraper.greet_candidate(candidate_contact)
