import threading, os, time, random
from config import Config
from utils.logger import log
from models.boss_scraper import BossScraper
from models.proxy_scraper import ProxyScraper
from models.geek import Geek

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

    def format_index_total(self, index, total):
        return "{}/{}".format(index, total)

    def scrape_for_job(self, scraper, job_id):
        log(f"🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉开始抓取简历🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
        job = scraper.get_job_description(job_id)
        if not job:
            log(f"❌❌❌❌❌❌未获得职位描述信息，程序停止~请检测登录是否过期。", level='error')
            return
        
        candidates = scraper.get_recommended_candidates(job_id)
        filtered_candidates = scraper.filter_candidates(job, candidates)
        candidates_total = len(filtered_candidates)
        log(f'-------- 已初步筛选出 [{candidates_total}] 份简历 -------- ')
        for index, candidate in enumerate(filtered_candidates, start=1):
            # 防止被封
            log(f"-----获取牛人简历详情：开始抓取 [{candidate['geekCard']['geekName'] if candidate['geekCard'] and 'geekName' in candidate['geekCard'] else candidate['geekCard']['name']} {self.format_index_total(index, candidates_total)}] 的简历....")
            sleep_time = random.randint(10, 40)
            log(f'防止被封等待随机：[ {sleep_time} ] 秒...')
            time.sleep(sleep_time)
            geek = scraper.get_candidate_details(candidate)
            if scraper.compare_with_job(job, geek):
                scraper.greet_candidate(geek)

def main():
    # 获取当前脚本的目录
    log(f"🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉程序启动🎉🎉🎉🎉🎉🎉🎉🎉🎉🎉")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.abspath(os.path.join(current_dir, '..', 'config.ini'))
    config = Config(filepath=config_path)
    if not config or not config.jobs_id or len(config.jobs_id)<=0:
        log(f"❌❌❌❌❌❌未配置待招聘职位，程序停止~请检查根目录的 .ini 配置文件。", level='error')
        return
    log(f"🍋🍋🍋🍋🍋🍋解析 .ini 配置完成")
    scraper = JobScraper(config)
    scraper.scrape_and_message()

if __name__ == "__main__":
    main()
