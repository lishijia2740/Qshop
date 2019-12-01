#重写数据库的路由配置


## db_for_read  读取使用的库
## db_for_write  写入使用的库


class Router(object):
    def db_for_read(self, model, **hints):
        return "slave"

    def db_for_write(self, model, **hints):
        return "default"