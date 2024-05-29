import time, random, json, re
from models.base_scraper import BaseScraper
from utils import fileutils
from utils import utils
import settings
from models.geek import Geek
from models.job import Job
from utils.logger import log

class BossScraper(BaseScraper):
    def __init__(self, config):
        # 经验和学历不分招聘职位了
        self.config = config
        self.headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8",
            "Cookie": f"{utils.create_cookie_header(config.cookie)}",
            "Dnt": "1",
            "Priority": "u=1, i",
            "Referer": "https://www.zhipin.com/",
            "Sec-Ch-Ua": "\"Chromium\";v=\"124\", \"Google Chrome\";v=\"124\", \"Not-A.Brand\";v=\"99\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"macOS\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "Token": "phvmkeqH2VnOjfv",
            "Traceid": "0EEBBE2F-A50A-476C-AD55-8EDC90764940",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "X-Anti-Request-Token": "",
            "X-Requested-With": "XMLHttpRequest",
            "Zp_token": "V1RtIhFOL-3FlgXdJoyR4QKCyw6jnWxg~~"
        }


    def get_job_description(self, job_id):
        """
        获取职位描述
        """
        # 1. 从缓存文件获取职位描述
        log(f"-----获取职位描述：开始获取职位描述....")
        job_description_filepath = self.OUTPUT_PATH + job_id + '.job_description'
        job = fileutils.load_obj_from_file(job_description_filepath)
        if not job:
            # 请求网络
            _ = utils.get_request(self.config.job_detail_url + f"?encJobId={job_id}", self.headers)
            if _['code'] == 0:
                log(f"🍋🍋🍋🍋🍋获取职位描述: [{job_id}] {self.config.job_name} 的职位描述，网络获取成功。")
                j = Job(_['zpData']['job'])
                j.skill_list = _['zpData']['skillList']
                job =j
                # 存入文件
                fileutils.save_obj_to_file(job, job_description_filepath)
            else:
                log(f"🚫🚫🚫🚫🚫🚫获取职位描述: [{job_id}] {self.config.job_name} 的职位描述，网络获取失败。Error：",_['message'], 'error')
        return job
    
    def get_recommended_candidates(self, job_id):
        if random.randint(1, 5) < 3 and self.config.geek_search_url:
            log(f"😏😏😏😏😏😏 防封随时: 开始抓取'搜索牛人'的简历....")
            return self.get_geeks_search(job_id)
        else:
            log(f"😈😈😈😈😈😈 防封随机: 开始抓取‘推荐牛人’的简历....")
            return self.get_geeks_recommended(job_id)

    def get_geeks_recommended(self, job_id):
        """
        获取牛人推荐列表
        """
        candidates = []
        # 防止被封
        page_num = random.randint(2, 4)
        log(f"-----获取牛人推荐列表: 开始抓取简历....")
        for page in range(1, page_num):
            # 防止被封
            log(f"-----获取牛人推荐列表: 开始抓取第 [{page}/{page_num-1}] 页的简历....")
            time.sleep(random.randint(5, 30))
            _ = utils.get_request(self.config.geek_list_url + f"&page={page}&jobId={job_id}", self.headers)
            if _['code'] == 0:
                log(f"🍋🍋🍋🍋🍋获取牛人推荐列表: 第 [{page}]/{page_num-1} 页的简历获取成功....")
                candidates.extend(_['zpData']['geekList'])
            else:
                log(f'🚫🚫🚫🚫🚫🚫获取牛人推荐列表：第 [{page}]/{page_num-1} 页的简历获取失败，Error:\n',_['message'], 'error')
        return candidates
    
    def get_geeks_search(self, job_id):
        """
        获取搜索列表
        """
        candidates = []
        # 防止被封
        page_num = random.randint(2, 5)
        page_num = 2
        log(f"-----获取搜索列表: 开始抓取简历....")
        for page in range(1, page_num):
            log(f"-----获取搜索荐列表: 开始抓取第 [{page}/{page_num-1}] 页的简历....")
            _ = utils.get_request(self.config.geek_search_url + f"&page={page}&jobId={job_id}", self.headers)
            if _['code'] == 0:
                log(f"🍋🍋🍋🍋🍋获取搜索列表: 第 [{page}/{page_num-1}] 页的简历获取成功....")
                candidates.extend(_['zpData']['geeks'])
            else:
                log(f'🚫🚫🚫🚫🚫🚫获取搜索列表：第 [{page}/{page_num-1}] 页的简历获取失败，Error:\n',_['message'], 'error')
        return candidates


    def get_candidate_details(self, candidate):
        """
        获取候选人详情
        """
        if not candidate or not candidate['geekCard']:
            log('🚫🚫🚫🚫🚫🚫获取牛人简历详情：get_candidate_details candidate is error.', 'error')
            return
        exceptId = candidate['geekCard']['expectId']
        jid = candidate['geekCard']['jobId']
        lid = candidate['geekCard']['lid']
        securityId = candidate['geekCard']['securityId']
        _ = utils.get_request(self.config.geek_info_url + f"&expectId={exceptId}&jid={jid}&lid={lid}&securityId={securityId}", self.headers)
        if _['code'] == 0:
            log(f"🍋🍋🍋🍋🍋获取牛人简历详情：抓取 [{candidate['geekCard']['geekName'] if candidate['geekCard'] and 'geekName' in candidate['geekCard'] else candidate['geekCard']['name']}] 的简历成功❤")
            g = Geek(_['zpData']['geekDetailInfo'])
            g.except_id = exceptId
            g.lid = lid
            g.jid = jid
            g.security_id = securityId
            return g
        else:
            log(f"🚫🚫🚫🚫🚫🚫获取牛人简历详情：抓取 [{candidate['geekCard']['geekName'] if candidate['geekCard'] and 'geekName' in candidate['geekCard'] else candidate['geekCard']['name']}] 的简历失败", 'error')
        return None
    def filter_candidates(self, job, candidates):
        """
        粗略筛选候选人
        """
        # 根据基本信息简单筛选候选人
        filtered_candidates = [candidate for candidate in candidates if self.is_suitable(job, candidate)]
        return filtered_candidates

    def compare_with_job(self, job, geek):
        """
        利用大模型对比和筛选候选人
        """
        # 使用大模型比对职位描述和候选人详情
        # 假设有个大模型 API 接口
        # {geek.generate_resume()}
        # 牛人简历
        # geek_resume = geek.generate_resume()

        # 先筛选如果是大专，且工作经验小于5年，自动忽略
        if geek.degree == 202 and geek.work_years < 5:
            log(f'>>>>>>>>>>>>>>>[{geek.name} {geek.degree_str} 工作年限：{geek.work_years}年，自动忽略~]')
            return False

        prompt = f"""
            Now you want to recruit a {job.job_name}. You are an expert in your field.  You need to evaluate the candidate's resume against the requirements of the position.
            Your output must be in the following format, and please use Chinese for the reasons:
            {{
                "evaluation": "your evaluation",
                "reason": "The reason for your evaluation"
            }}
            If you think the candidate is very capable, your evaluation is A, and the output is in the 'evaluate' field; if the candidate is capable, your evaluation is B, and the output is in the 'evaluate' field; if the candidate is incompetent, Your evaluation is C, and the output is in the 'evaluate' field; if the candidate is completely unqualified, your evaluation is D, and the output is in the 'evaluate' field. And in the 'reason' field, output the reason for your evaluation in Chinese.

            ******************
            The following are the requirements for this recruitment position:
            {job.generate_job_desc()}

            Here is the candidate's resume:
            {geek.generate_resume()}
        """

        body = {
            "model": f"{settings.MODEL}",
            "stream": False,
            "format":"json",
            "prompt": prompt
        }

        log(f"-----大模型比对：开始大模型比对 [{geek.name}] 的简历....")
        _ = utils.post_request(settings.MODEL_BASE_URL, json_data=body)
        evaluation = 'E'
        reason = '未评价'
        if 'response' in _:
            try:
                log('---------大模型比对结果-----------\n',_['response'])
                res = json.loads(_['response'])
                if res and 'evaluation' in res:
                    evaluation = res['evaluation']
                if res and 'reason' in res:
                    reason = res['reason']
            except:
                log('🚫🚫🚫🚫🚫🚫大模型返回 response 数据异常.', 'error')
                log(f"🚫🚫🚫🚫🚫🚫大模型比对：大模型比对 [{geek.name}] 的简历失败，请查看大模型服务。", 'error')
                res = None
            
        # 缓存简历 [20240512][A]王二小.txt
        cretetime = time.strftime("%Y%m%d %H%M", time.localtime())
        fileutils.save_data_to_file(f"{self.OUTPUT_PATH}[{cretetime}][{evaluation}]{geek.name}.txt", geek.generate_resume() + f"\n\n评价：\n[{evaluation}]\n" + reason)
        return evaluation == 'A' or evaluation == 'B' or evaluation == 'E'
        
    def greet_candidate(self, geek):
        """
        与候选人打招呼
        """
        body = {
            "gid": geek.encrypt_geek_id,
            "jid": geek.encrypt_jid,
            "lid": geek.lid,
            "suid":'',
            "from":'',
            "expectId": geek.except_id,
            "securityId": geek.security_id
        }
        log(f"-----与牛人打招呼：开始和 [{geek.name}] 打招呼....")
        res = utils.post_request(self.config.chat_start_url, self.headers, data=body)
        if res['code'] == 0 and res['zpData']['status'] == 1:
            # {'code': 0, 'message': 'Success', 'zpData': {'status': 2, 'stateDes': '稍后再试', 'data': {'status': 2}}}
            log(f"🍋🍋🍋🍋🍋与牛人打招呼：和 [{geek.name}] 打招呼成功，等待牛人回复...")
        else:
            log(f"🚫🚫🚫🚫🚫🚫与牛人打招呼：和 [{geek.name}] 打招呼失败，请尽快检查登录是否过期。", level='error')
            log(res, level='error')

    def is_suitable(self, job, candidate):
        # 求职状态不是’在职-暂不考虑‘ and 意向地点是南京 
        # 工作年限先忽略
        try:
            log(f"-----粗略筛选简历：开始筛选 [{candidate['geekCard']['geekName']}] 的简历....")
            if candidate['geekCard']['applyStatus'] != 1 and candidate['geekCard']['expectLocationCode'] == job.location and candidate['geekCard']['expectPositionCode'] == job.position and candidate['geekCard']['geekGender'] == 1:
                school = candidate['geekCard']['geekEdu']['school']
                pattern = r'[\u4e00-\u9fa5]+大学[\u4e00-\u9fa5]+学院|[\u4e00-\u9fa5]+职业[\u4e00-\u9fa5]+'
                if re.match(pattern, school):
                    log(f"🚫🚫🚫🚫🚫🚫粗略筛选简历，院校不通过：[{candidate['geekCard']['geekName']}][{school}] 的简历不通过. [{'男' if candidate['geekCard']['geekGender'] == 1 else '女'}][{candidate['geekCard']['expectLocationName']}][{candidate['geekCard']['expectPositionName']}]{candidate['geekCard']['applyStatusDesc']}", level='warning')
                    return False
                log(f"🍋🍋🍋🍋🍋粗略筛选简历：[{candidate['geekCard']['geekName']}][{school}] 的简历通过 ➠ 已加入简历库！")
                return True
        except:
            # 默认 or 如果来自搜索，则自动通过粗略筛选
            return True
        log(f"🚫🚫🚫🚫🚫🚫粗略筛选简历：[{candidate['geekCard']['geekName']}][{school}] 的简历不通过. [{'男' if candidate['geekCard']['geekGender'] == 1 else '女'}][{candidate['geekCard']['expectLocationName']}][{candidate['geekCard']['expectPositionName']}]{candidate['geekCard']['applyStatusDesc']}", level='warning')
        return False



