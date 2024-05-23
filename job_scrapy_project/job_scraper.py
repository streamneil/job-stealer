import threading, os, time, random
from config import Config
from models.boss_scraper import BossScraper
from models.proxy_scraper import ProxyScraper

class JobScraper:

    def __init__(self, config):
        self.config = config
        self.scrapers = {
            'boss': ProxyScraper(BossScraper(config))
        }

    def scrape_and_message(self):
        threads = []
        for job_id in self.config.jobs_id:
            for site in self.scrapers:
                scraper = self.scrapers[site]
                thread = threading.Thread(target=self.scrape_for_job, args=(scraper, job_id))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

    def scrape_for_job(self, scraper, job_id):
        job_description = scraper.get_job_description(job_id)
        candidates = scraper.get_recommended_candidates(job_id)
        filtered_candidates = scraper.filter_candidates(job_description, candidates)
        for candidate in filtered_candidates:
            # 防止被封
            time.sleep(random.randint(10, 40))
            candidate_details = scraper.get_candidate_details(candidate)
            if scraper.compare_with_job(job_description, candidate_details):
                print('简历筛选通过')
                scraper.greet_candidate(candidate)

def main():
    # 获取当前脚本的目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(current_dir, '..', 'config.ini'))
    config = Config(filepath=config_path)
    if not config or not config.jobs_id or len(config.jobs_id)<=0:
        print('未配置招聘职位')
        return
    scraper = JobScraper(config)
    # scraper.scrape_and_message()

if __name__ == "__main__":
    main()
