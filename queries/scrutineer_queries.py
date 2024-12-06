import pymysql
import config
from queries import general_queries
from datetime import date

async def get_list_comp(tg_id):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            cur.execute(f"SELECT compName, compId, date2 FROM competition WHERE scrutineerId = {tg_id} and isActive = 1")
            competitions = cur.fetchall()
            cur.close()
            ans = []
            now = date.today()
            for comp in competitions:
                a = now - comp['date2']
                if a.days <= 0:
                    ans.append(comp)
            return ans
    except Exception as e:
        print(e)
        print('Ошибка выполнения запроса на поиск соревнований для chairman1')
        return 0



async def get_Chairman(tg_id):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            active_comp_id = await general_queries.get_CompId(tg_id)
            cur.execute(f"SELECT chairman_Id FROM competition WHERE compId = {active_comp_id}")
            chairman_id = cur.fetchone()
            cur.close()
            return chairman_id['chairman_Id']
    except:
        print('Ошибка выполнения запроса поиск chairman')
        return 0


async def set_active_0(user_id):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        active_comp = await general_queries.get_CompId(user_id)
        with conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE competition_judges set active = 0, is_use = 0 WHERE compId = {active_comp}")
            conn.commit()
        return 1
    except:
        return 0

async def check_chairman_pin(tg_id, pin, mode):
    try:
        conn = pymysql.connect(
            host=config.host,
            port=3306,
            user=config.user,
            password=config.password,
            database=config.db_name,
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn:
            cur = conn.cursor()
            cur.execute(f"select PinCode, compId from competition where isActive = 1")
            ans = cur.fetchall()
            status, compid = 0, -1
            for comp in ans:
                if comp['PinCode'] == pin:
                    status, compid = 1, comp['compId']
                    break

            if status == 1:
                if mode == 0:
                    sql = "INSERT INTO skatebotusers (`tg_id`, `Id_active_comp`, `status`, `active`) VALUES (%s, %s, %s, %s)"
                    cur.execute(sql, (tg_id, compid, 3, 1))
                    conn.commit()

                cur.execute(f"update competition set chairman_Id = {tg_id} where compId = {compid}")
                conn.commit()
                if mode == 1:
                    cur.execute(f"update skatebotusers set Id_active_comp = {compid} where tg_id = {tg_id}")
                    conn.commit()
                return 1
        return 0
    except Exception as e:
        return -1
