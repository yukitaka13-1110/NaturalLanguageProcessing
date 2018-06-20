from DataFormat import Report
from DataBase import DB

""" インスタンスを作成する """
def make_report_instance(db_name):
    db = DB(db_name)
    report_lst,inst_lst = db.fetchall(),[]
    for r in report_lst:
        studentID,year,month,day,subject,score,c1,c2,c3 = r
        report = Report(studentID,year,month,day,subject,score,c1,c2,c3)
        inst_lst.append(report)
    db.close()
    return inst_lst

""" 条件でインスタンスをフィルタリング """
def inst_filter(inst_lst,studentID=None,low=0,high=100,subject=None,begin='2015/7',end='2017/2'):
    lst = []
    for inst in inst_lst:
        if studentID is not None:
            if not inst.is_studentID_equal(studentID):
                continue
        if subject is not None:
            if not inst.is_subject_equal(subject):
                continue
        if inst.is_score_in_range(low,high) and inst.is_date_in_range(begin,end):
            lst.append(inst)
    return lst

def main():
    ########################################
    #       reportインスタンスの作成       #
    ########################################
    db_name = 'CommentData.db'
    inst_lst = make_report_instance(db_name)

    ########################################
    #         やりたいこと書いて           #
    ########################################
    lst = inst_filter(inst_lst,studentID='shima001',begin='2016/4',end='2016/6')
    for inst in lst:
        print(inst.studentID())
        print(inst.score())
        print(inst.subject())
        words = inst.parse_comment_if(1,'047')
        print(words)
    return


if __name__ == '__main__':
    main()
