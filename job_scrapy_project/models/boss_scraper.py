import requests, time, random
from models.base_scraper import BaseScraper
from utils import fileutils
from utils import utils
import settings

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
            "Referer": "https://www.zhipin.com/web/frame/recommend/?filterParams=&t=&inspectFilterGuide=&version=5305&status=0&jobid=5c1b41c751c520a01n193dq8FlRR&source=0",
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
        job_description_filepath = self.OUTPUT_PATH + job_id + '.job_description'
        job_description = fileutils.get_file_content(job_description_filepath)
        if not job_description:
            # 请求网络
            _ = utils.get_request(f"{self.config.job_detail_url}?encJobId={job_id}", self.headers)
            if _['code'] == 0:
                job_data = _['zpData']['job']
                job_description = (
                    f"职位名称：{job_data['jobName']}\n"
                    f"职位类型：{job_data['positionName']}\n"
                    f"城市名称：{job_data['locationName']}\n"
                    f"经验：{self.config.experience}\n"
                    f"学历：{self.config.educational_level}\n"
                    f"薪资范围：{job_data['lowSalary']}K-{job_data['highSalary']}K\n"
                    # f"职位关键词：{', '.join(job_data['skillList'])}\n"
                    f"职位描述：{job_data['postDescription']}"
                )
                # 存入文件
                fileutils.save_data_to_file(job_description_filepath, job_description)
        return job_description

    def get_recommended_candidates(self, job_id):
        """
        获取牛人推荐列表
        """
        candidates = []
        # 防止被封
        page_num = random.randint(2, 5)
        for page in range(1, page_num):
            # 防止被封
            time.sleep(random.randint(5, 30))
            _ = utils.get_request(f"{self.config.geek_list_url}&page={page}&jobId={job_id}", self.headers)
            if _['code'] == 0:
                candidates.extend(_['zpData']['geekList'])
            else:
                print('xxxxx[获取牛人推荐列表错误]xxxxx:',_['message'])
        return candidates

    def get_candidate_details(self, candidate):
        """
        获取候选人详情
        """
        if not candidate or not candidate['geekCard']:
            print('xxxxx【错误】xxxxx get_candidate_details candidate is error.')
            return
        exceptId = candidate['geekCard']['expectId']
        jid = candidate['geekCard']['jobId']
        lid = candidate['geekCard']['lid']
        securityId = candidate['geekCard']['securityId']
        _ = utils.get_request(f"{self.config.geek_info_url}&expectId={exceptId}&jid={jid}&lid={lid}&securityId={securityId}", self.headers)
        if _['code'] == 0:
            return self.generate_candidate_resume(_['zpData']['geekDetailInfo'])
        else:
            print('xxxxx[获取候选人详情错误]xxxxx:')
        return None

    def generate_candidate_resume(self, candidate_info):
        """
        封装候选人简历
        """
        candidate_resume = {
            f"姓名：\n"
            f"年龄：\n"
            f"学历：\n"
            f"工作地点：\n"
            f"期望薪资：\n"
            f"自我评价：\n"
            f"毕业院校：\n"
            f"工作年限：\n"
            f"工作经验：\n"
            f"项目经验：\n"
        }
        return candidate_resume

    def filter_candidates(self, job_description, candidates):
        """
        粗略筛选候选人
        """
        # 根据基本信息简单筛选候选人
        filtered_candidates = [candidate for candidate in candidates if self.is_suitable(job_description, candidate)]
        return filtered_candidates

    def compare_with_job(self, job_description, candidate_details):
        """
        利用大模型对比和筛选候选人
        """
        # 使用大模型比对职位描述和候选人详情
        # 假设有个大模型 API 接口
        # TODO 真实比较简历
        job_description = """
            学历要求：不低于本科
            工作年限：不少于5年
            岗位职责：
            1、负责Android手机的应用开发, 负责软件的设计、开发、需求分析等；
            2、负责产品的功能模块的详细设计、编码实现和单元测试，保证开发进度；
            3、完成与工作相关文档的编写；
            4、参与Android系统新特性、新功能和新场景的研究；

            任职条件：
            1、精通JAVA、Kotlin语言，熟悉Android平台及框架，3年以上实际开发经验；
            2、熟练掌握常用的技术框架，如网络请求框架（Retrofit或其他）、事件总线框架（eventbus或其他）、数据库框架（ObjectBox或其他，比如：GreenDao、Room等）；
            3、熟练掌握响应式编程框架RxJava；
            4、熟练掌握MVVM架构及相关框架，如ViewModel、LiveData、Lifecycles等；
            5、有组件化开发经验优先；
            6、有进程/协程/多线程/编程经验，熟悉Socket网络编程，熟悉TCP/IP，HTTP等网络协议。
            7、具备Flutter项目开发经验；
            8、具备鸿蒙应用开发技能，并有积极的学习热情；

        """

        candidate_details = """
            王亚奇
            24岁
            在职-暂不考虑
            期望薪资：13-15K
            应聘岗位：Android工程师
            河南工业大学
            计算机科学与技术
            本科
            2021年毕业
            工作年限：3年
            个人描述："1、有多个项目经验、熟悉 MVP，MVVM模式、可熟练运用单例、工厂、建造者、代理等设计模式；2、熟练掌握自定义控件、View的测量、布局、事件分发机制、Handler\n消息机制；3、了解APP运行过程中内存泄漏和内存溢出问题原因；4、熟悉Handler、OkhttpClient相关源码。"
            工作经历：
            1. 南京鼎捷软件科技有限公司
            时间：2022.8-至今 
            职责："1、负责移动平台功能开发维护。\n2、重构代码，保证代码的可读性，易维护性。\n3、配合测试人员完成测试。\n4、负责应用的屏幕适配。"
        """

        prompt = f"""
            Now you want to recruit a {self.config.job_name}, you are an expert in this field. You need to screen job candidate' resumes based on the description of job requirements for this position.
            If you think the candidate is very competent, your evaluation is A; if the candidate is competent, your evaluation is B; if the candidate is incompetent, your evaluation is C; if the candidate is completely unqualified, your evaluation is D.

            Please output in the following format:            
            {{
                "evaluation": "",
                "reason": ""
            }}

            ***************
            This is the description of the position to be recruited:
            {job_description}

            This is the candidate's resume:
            {candidate_details}

        """

        body = {
            "model": f"{settings.MODEL}",
            "stream": False,
            "format":"json",
            "prompt": prompt
        }

        response = utils.post_request(settings.MODEL_BASE_URL, body=body)
        if response and response['response'] and response['response']['evaluation']:
            evaluation = response['response']['evaluation']
        else:
            evaluation = 'E'
        
        # 缓存简历 [20240512][A]王二小.txt
        cretetime = time.strftime("%Y%m%d", time.localtime())
        fileutils.save_data_to_file(f"[{cretetime}][{evaluation}]{self.OUTPUT_PATH}{candidate_details['name']}.txt", candidate_details)
        return evaluation == 'A' or evaluation == 'B'
        
    def greet_candidate(self, candidate):
        """
        与候选人打招呼
        """
        # TODO 打招呼
        body = {

        }
        utils.post_request(f"{self.config.chat_start_url}", self.headers, body=body)

    def is_suitable(self, job_description, candidate):
        # 求职状态不是’在职-暂不考虑‘ and 意向地点是南京 
        # 工作年限先忽略
        return candidate['geekCard']['applyStatus'] != 1 and candidate['geekCard']['expectPositionCode'] == 100202



