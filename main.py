import time

import httpx
from httpx import Cookies
import random
from typing import List, Dict, Tuple

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 '
                  'Safari/537.36',
    'origin': 'http://2.shikong.info:8089/',
    'cookie': '',
    'Connection': 'close',
    'referer': 'http://2.shikong.info:8089/'
}
cookie = None
cookie_dict = {'u1': '', 'u2': '', 'u3': ''}
haixian = ['金鱼', '海马', '小玄武']
wuxing = ['金', '木', '水', '火', '土']
exp_use = [52]
# 目前天神31，三星成长魂石26，百变国庆66
merge_property_use = [31, 26, 66]
sub_pet_list = []
to_merge_sub_pet = []
merge_main_pet = {}
merge_pet_except : List[str] = ['19']
pack_pet = []
divine_pet_except = ['炽天使', '玛雅宝宝', '安吉', '海之音', '双翼天使妖妖', '音速瑾', '青影龙', '仲裁', '影娅瑟',
                     '蜡笔', '兔儿啾啾', '自然女神', '圣火麒麟', '亲吻鱼', '琉璃狐仙', '铁骑战', '召唤之龙', '白虎女神',
                     '浴火之凤', '罗刹魔女', 'k歌霸王龙', '天使妖妖', '月之征兆', '佑碧', '睡美人雅雅', '恶魔邪灵', '伪暗天使',
                     '圣诞龙', '年兽', '寒江雪', '雪域之凤', '鬼精灵', '双子星耀', '花仙子', '金羽神凤', '鹦鹉',
                     '虎妞', '古木精', '亲吻鱼', '兔啦花花', '科学怪人', '托里兹', '神龙媚若', '萌萌', '圣兽云鹿',
                     '潜魔兽', '加藤鹰', 'GM鸭子', '蝶', '莉莉丝', '蛇魔丝西娜', '草莓', '小不点', '马鲁斯',
                     '圣诞龙', '终极斑', '猫女神', '涅槃兽', '', '', '', '', '',
                     '', '', '', '', '', '', '', '', '',]
divine_pet_available_use = ['射手木偶', '狂战神', '童童木', '熊猫ORZ', '吕布', '铁骑战', '彩灯仙子']
if_start = True


def init_cookies(cookie_dict: dict):
    c = Cookies()
    for k, v in cookie_dict.items():
        c.set(name=k, value=v, domain="http://2.shikong.info:8089/")
    return c


def extract_content_between_brackets(s):
    start = s.find("[")
    if start == -1:
        return None

    stack = []
    end = start + 1

    for i in range(start + 1, len(s)):
        if s[i] == "[":
            stack.append("[")
        elif s[i] == "]":
            if not stack:
                end = i
                break
            stack.pop()

    if not stack:
        return s[start + 1:end]
    else:
        return None


def login(username: str, password: str):
    with open("userdata.txt", 'r', encoding='utf-8') as userdata:
        c = userdata.read()
        c = eval(c)
    if testLoginStatus(c):
        print("测试登陆状态成功!")
        return True
    else:
        login_url = f"http://2.shikong.info:8089/api/login?username={username}&password={password}"
        response = httpx.get(login_url, headers=headers, timeout=8.0)
        login_status = response.text.strip('\"')
        print(login_status)
        if login_status == '登录失败！操作繁忙！':
            time.sleep(10 + random.random() * 2)
            response = httpx.get(login_url, headers=headers, timeout=8.0)
            login_status = response.text.strip('\"')
        cookie_dict['u2'] = login_status
        print(cookie_dict)
        with open("userdata.txt", 'w', encoding='utf-8') as userdata:
            userdata.write(str(cookie_dict))
        init_cookies(cookie_dict)
        return True


def testLoginStatus(cookies: dict) -> bool:
    cookie_dict['u1'] = cookies['u1']
    cookie_dict['u2'] = cookies['u2']
    cookie_dict['u3'] = cookies['u3']
    init_cookies(cookie_dict)
    print(cookie_dict)
    url = f"http://2.shikong.info:8089/api/getMapInfo?username=username={cookie_dict['u1']}&password={cookie_dict['u2']}&random={random.random()}&mapID=1"
    response = httpx.get(url, headers=headers, cookies=cookie, timeout=8.0)
    if response.text.find("message") > -1:
        return False
    return True


def getPetList(type: str = 'p') -> list:
    # type -p为仓库 -pack为背包
    get_pet_list_url = f"http://2.shikong.info:8089/api/getPetList?username={cookie_dict['u1']}&password={cookie_dict['u2']}&Type={type}&random={random.random}"
    response = httpx.get(get_pet_list_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    if type == 'pack':
        result = '[' + extract_content_between_brackets(result) + ']'
    result = result.replace('null', '0')
    result = result.replace('false', 'False')
    print(result)
    return eval(result)


def carryPet(id: int):
    carry_pet_url = f"http://2.shikong.info:8089/api/getPet?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&random={random.random}"
    response = httpx.get(carry_pet_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    print(result)


def sendPet(id: int):
    sent_pet_url = f"http://2.shikong.info:8089/api/addPasture?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&random={random.random}"
    response = httpx.get(sent_pet_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    print(result)


def changePetToFirst(id: int):
    change_pet_to_first_url = f"http://2.shikong.info:8089/api/getJH?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&random={random.random}"
    response = httpx.get(change_pet_to_first_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    print(result)


def useProperty(id: int):
    use_property_url = f"http://2.shikong.info:8089/api/useProp?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&random={random.random}"
    response = httpx.get(use_property_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    print(result)


def mergePet(id: int, id1: int, pid: int, pid1:int):
    merge_pet_url = f"http://2.shikong.info:8089/api/Hecheng?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&id1={id1}&pid={pid}&pid1={pid1}&random={random.randint(1000000,9999999)}"
    response = httpx.get(merge_pet_url, headers=headers, cookies=cookie, timeout=8.0)
    result = response.text.strip('\"').replace("\\", "")
    print(result)
    if result.find("恭喜您") != -1:
        return True
    return False


def divinePet(id: int, id1: int, np: int, pid: int, pid1: int):
    divine_pet_url = f'''http://2.shikong.info:8089/api/Niepang?username={cookie_dict['u1']}&password={cookie_dict['u2']}&id={id}&id1={id1}&pid={pid}&pid1={pid1}&np={np}&random={random.randint(1000000,9999999)}'''
    response = httpx.get(divine_pet_url)
    result = response.text.strip('\"').replace("\\", "")
    print(result)
    if result.find("恭喜您") != -1:
        return True
    return False


# 检查等级，使用背包中所有宠物使用经验道具
# TODO: 经验道具是否用完的检查
def levelUpPet():
    pack_pet = getPetList('pack')
    while True:
        for pet in pack_pet:
            if pet.get('等级', 1) < 40:
                changePetToFirst(pet.get("宠物序号", 0))
                if exp_use is not None:
                    useProperty(exp_use[0])
        pack_pet = getPetList('pack')
        flag = True
        for pet in pack_pet:
            if pet.get('等级', 1) < 40:
                flag = False
        if flag:
            break


# 刷新合宠列表
# 1. 只要主宠列表：选出五系宠中成长最高的（被排除的不算）
# 2. 只要副宠列表：需要提供主宠，如果不提供方法默认执行失败；从符合条件的宠物（比如海鲜）中选择，返回剔除掉主宠和排除宠后的结果
# 3. 主副宠都要：上述两过程结合
# TODO:获取合成副宠，默认为海鲜
def chooseMergePet(type: str = 'main', main_pet_id: str = None, sub_pet_names: List[str] = None) -> Tuple[Dict, List[Dict]]:
    # 获取宠物列表，筛选出属性为五行的宠物
    pet_list = getPetList()
    pet_list.extend(getPetList('pack'))
    temp_list = []
    for pet in pet_list:
        # 排除设置的宠物 或 属性不为五行的宠物
        if isinstance(pet["类型缓存"], list) and pet["类型缓存"]["系别"] in wuxing:
            temp_list.append(pet)
        elif pet.get('五行', '') in wuxing:
            temp_list.append(pet)
    pet_list = []
    for pet in temp_list:
        if pet.get('宠物序号', '') not in merge_pet_except:
            pet_list.append(pet)
    print(f'筛选后的宠物1：{temp_list}')
    print(f'筛选后的宠物2：{pet_list}')
    # 进行主宠副宠的选择
    merge_main_pet = {}
    for pet in pet_list:
        # 获取合成主宠，默认为五行为金木水火土中成长最高的
        if pet.get('成长', 0) > merge_main_pet.get('成长', 0):
            merge_main_pet = pet
    pet_list.remove(merge_main_pet)
    print(f'主宠：{merge_main_pet}')
    print(f'副宠：{pet_list}')
    if type == 'main':
        return merge_main_pet
    elif type == 'sub':
        return pet_list
    elif type == 'main,sub':
        return merge_main_pet, pet_list
    return {}, []


# 登录
login(cookie_dict['u1'], cookie_dict['u3'])
chooseMergePet()
while if_start or len(sub_pet_list) > 0:
    if_start = False
    # 获取宠物列表
    pet_list = getPetList()
    pet_list.extend(getPetList('pack'))
    merge_main_pet, sub_pet_list = chooseMergePet('main,sub')
    # 整理背包宠物，带出一主宠两副宠
    pack_pet = getPetList('pack')
    changePetToFirst(pack_pet[0].get('宠物序号', 0))
    for pet in pack_pet[1:]:
        sendPet(pet.get("宠物序号", 0))
    carryPet(merge_main_pet.get("宠物序号", 0))
    changePetToFirst(merge_main_pet.get("宠物序号", 0))
    pack_pet = getPetList('pack')
    for pet in pack_pet:
        if pet.get("宠物序号", 0) != merge_main_pet.get("宠物序号", 0):
            sendPet(pet.get("宠物序号", 0))
    if len(sub_pet_list) >= 2:
        to_merge_sub_pet.append(sub_pet_list.pop())
        to_merge_sub_pet.append(sub_pet_list.pop())
        carryPet(to_merge_sub_pet[0].get('宠物序号', 0))
        carryPet(to_merge_sub_pet[1].get('宠物序号', 0))
    elif len(sub_pet_list) == 1:
        to_merge_sub_pet.append(sub_pet_list.pop())
        carryPet(to_merge_sub_pet[0].get('宠物序号', 0))
    else:
        raise ValueError("所有宠物已合成完毕！")

    # 检查等级，使用经验道具
    levelUpPet()
    time.sleep(2)

    # 合成宠物
    # TODO:判断合成道具是否足够
    while len(to_merge_sub_pet) > 0:
        if merge_main_pet.get('成长', 0) < 111:
            flag = mergePet(merge_main_pet.get('宠物序号', 0), to_merge_sub_pet[0].get('宠物序号', 0), merge_property_use[0],
                            merge_property_use[1])
        # elif merge_main_pet.get('成长', 0) >= 56.5:
        #     flag = mergePet(merge_main_pet.get('宠物序号', 0), to_merge_sub_pet[0].get('宠物序号', 0), merge_property_use[2],
        #                     merge_property_use[1])
        if flag:
            # 合成成功后更新宠物背包
            # TODO:合成后更新合成主宠
            pack_pet = getPetList('pack')
            to_merge_sub_pet.pop(0)
            levelUpPet()
            # TODO:判断是否出神宠(比如提前出神或百变出神)
        time.sleep(4.0 + random.random() * 2)