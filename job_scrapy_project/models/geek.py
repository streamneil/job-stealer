class Geek:
    """
    封装候选人信息的类
    """
    def __init__(self, candidate_info):
        if not candidate_info:
            return
        self.name = candidate_info['geekBaseInfo']['name']
        self.age_desc = candidate_info['geekBaseInfo']['ageDesc']
        self.degree_category = candidate_info['geekBaseInfo']['degreeCategory']
        self.work_years = candidate_info['geekBaseInfo']['workYears']
        self.certifications = [item['certName'] for item in candidate_info['geekCertificationList']]
        self.education_history = self.parse_geek_edu(candidate_info)
        self.work_experience = self.parse_geek_work_exp(candidate_info)
        self.position_experience = candidate_info['geekWorkPositionExpDescList']
        self.project_experience = self.parse_geek_proj_exp(candidate_info)
        self.expected_city = candidate_info['showExpectPosition']['locationName']
        self.applied_position = candidate_info['showExpectPosition']['positionName']
        self.expected_salary = candidate_info['showExpectPosition']['salaryDesc']
        self.self_description = candidate_info['geekBaseInfo']['userDescription']
        self.except_id = ''
        self.security_id = ''
        self.lid = ''
        self.jid = ''
        # 职位ID,打招呼使用
        self.encrypt_jid = candidate_info['encryptJid']
        self.user_id = candidate_info['geekBaseInfo']['userId']
        self.encrypt_geek_id = candidate_info['geekBaseInfo']['encryptGeekId']

    def parse_geek_edu(self, candidate_info):
        edu_exp = []
        for item in candidate_info['geekEduExpList']:
            edu_exp.append(f"[{item['degreeName']}] {item['startDate']}-{item['endDate']} {item['school']} {item['major']}")
        return edu_exp

    def parse_geek_work_exp(self, candidate_info):
        work_exp = []
        for item in candidate_info['geekWorkExpList']:
            work_exp.append(f"[{item['positionName']}] {item['startDate']}-{item['endDate']} {item['company']}\n职责:\n{item['responsibility']}")
        return work_exp

    def parse_geek_proj_exp(self, candidate_info):
        proj_exp = []
        for item in candidate_info['geekProjExpList']:
            proj_exp.append(f"项目名称：{item['name']}\n项目时间：{item['startDate']}-{item['endDate']}\n项目时长：{item['workYearDesc']}\n项目角色：{item['roleName']}\n项目描述：{item['projectDescription']}")
        return proj_exp

    def generate_resume(self):
        """
        生成并返回格式化的简历
        """
        resume = (
            f"姓名: {self.name}\n"
            f"年龄: {self.age_desc}\n"
            f"学历: {self.degree_category}\n"
            f"工作年限: {self.work_years}年\n"
            f"期望城市: {self.expected_city}\n"
            f"应聘职位: {self.applied_position}\n"
            f"期望薪资: {self.expected_salary}\n"
            f"自我评价: \n{self.self_description}\n"
            f"荣誉证书: {'; '.join(self.certifications) if self.certifications else '无'}\n"
            f"毕业院校:\n{'\n\n'.join(self.education_history)}\n"
            f"工作经验:\n{'\n\n'.join(self.work_experience) if self.work_experience else '未填写'}\n"
            f"职位经历:\n{'\n\n'.join(self.position_experience) if self.position_experience else '未填写'}\n"
            f"项目经验:\n{'\n\n'.join(self.project_experience if self.project_experience else '未填写')}\n"
        )
        return resume


    # 判断某字段是否存在于 JSON 数据中
    def check_field_exists(self, data, field):
        return field in data
    
# 使用示例
# 假设 candidate_info 是从某个 API 或数据库中获取的候选人信息字典
# candidate = GeekCandidate(candidate_info)
# log(candidate.generate_resume())