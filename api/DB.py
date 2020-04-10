import psycopg2


class PostgresDB():
    def __init__(self):
        self.conn = psycopg2.connect(database="testDB", user="postgres", password="123456", host="127.0.0.1", port="5432")
        self.cur = self.conn.cursor()

    # 表设计
    def table_info(self,table_name):
        tInfo={
            'mautd':{'column':[('date', 'dt'), ('timestamp without time zone', 'ts'), ('real', 'last')],
                     'index':['mautd_index','dt','ts']},
            'agtd':{'column':[('date', 'dt'), ('timestamp without time zone', 'ts'), ('real', 'last')],
                     'index':['agtd_index','dt','ts']}
        }
        if table_name not in tInfo:
            return False 
        return tInfo[table_name]

    # 获取表sql语句
    def table_sql(self,table_name,sql_type='table'):
        tInfo=self.table_info(table_name)
        if not tInfo:
            return False
        if sql_type=='table':
            sqlBody=""
            for c in tInfo['column']:
                sqlBody=sqlBody+c[1]+" "+c[0]+",\n"
                sql="create table %s (\n%s)"%(table_name,sqlBody[:-2])
            return sql
        if sql_type=='index':
            return "create unique index if not exists %s on %s(%s)"%(tInfo['index'][0],table_name,','.join(tInfo['index'][1:]))

    #表是否存在
    def has_table(self,table_name):
        if not self.table_info(table_name):
            print('表%s 不存在且没有预设'%(table_name))
            return -2
        #sql="select 1 from pg_tables where schemaname = 'public' and tablename = '%s';"%(table_name)
        sql='''
            SELECT
                format_type (A .atttypid, A .atttypmod) AS TYPE,
                A .attname AS NAME
            FROM
                pg_class AS C,
                pg_attribute AS A
            WHERE
                C .relname = '%s'
            AND A .attrelid = C .oid
            AND A .attnum > 0;
        '''%(table_name)
        self.cur.execute(sql)
        tInfo=self.cur.fetchall()
        if len(tInfo)==0:
            print('表%s 不存在但存在预设'%(table_name))
            return -1
        if tInfo!=self.table_info(table_name)['column']:
            print('表%s 存在但预设不符合'%(table_name))
            return 0
        print('表%s 存在'%(table_name))
        return 1

        # 创建表
    
    # 创建表
    def createTable(self,table_name):
       has_table=self.has_table(table_name)
       if has_table==-2:
           return False
       if has_table==0:
          self.cur.execute('drop index if exists %s'%(self.table_info(table_name)['index'][0]))
          self.cur.execute('drop table %s'%(table_name))
          print('删除表%s'%(table_name))
          has_table=-1
       if has_table==-1:
          self.cur.execute(self.table_sql(table_name,'table'))
          self.cur.execute(self.table_sql(table_name,'index'))
          print('创建表%s'%(table_name))
          self.conn.commit()
       return True

    # 插入
    def insertData(self,table_name,values):
        sql = "insert into %s values(%s)"%(table_name,','.join([str(v) for v in values]))
        self.cur.execute(sql)
        self.conn.commit()

    # 查询
    def select(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    # 清空表
    def truncate(self,table_name):
        sql="TRUNCATE %s"%(table_name)
        self.cur.execute(sql)
        self.conn.commit()

    # 关闭
    def close(self):
        self.cur.close()
        self.conn.close()    
        
        
    

