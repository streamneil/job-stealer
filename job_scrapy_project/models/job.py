import settings

class Job(object):
    """
    封装职位
    """
    def __init__(self, position_info):
        if not position_info:
            return
        # 位置code 101190100
        self.location = position_info['location']
        # 位置名称 南京
        self.location_name = position_info['locationName']
        self.skill_list = []
        #职位名称 "安卓开发工程师"
        self.job_name = position_info['jobName']
        # 职位code 100202
        self.position = position_info['position']
        # 职位名称 Android
        self.position_name = position_info['positionName']
        self.post_description = position_info['postDescription']
        self.low_salary = position_info['lowSalary']
        self.high_salary = position_info['highSalary']
        self.address_text = position_info['addressText']
        self.degree = position_info['degree']
        self.experience = position_info['experience']
        self.degree_str = settings.DEGRER_DICT.get(position_info['degree'], '未知')
        self.experience_str = settings.EXPERIENCE_DICT.get(position_info['experience'], '未知')

    def generate_job_desc(self):
        """
        生成职位描述
        """

        _ = (
            f"职位名称：{self.job_name}\n"
            f"职位类型：{self.position_name}\n"
            f"所在城市：{self.location_name}\n"
            f"具体地点：{self.address_text}\n"
            f"薪资范围：{self.low_salary}-{self.high_salary}K\n"
            f"工作经验：{self.experience_str}\n"
            f"学历要求：{self.degree_str}\n"
            f"技能要求：\n{'; '.join(self.skill_list)}\n"
            f"职位介绍：\n{self.post_description}\n"
        )

        return _





        