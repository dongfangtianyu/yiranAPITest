# 基于Pytest的自动化测试框架

这是一个花费四小时完成的接口自动化测试框架，拥有以下特性：

- [x] 支持pytest生态中各种插件
- [x] 自动记录接口通讯报文
- [x] 支持接口mock
- [x] 支持BaseURL切换测试环境
- [x] 支持多种来源的数据驱动测试(json/csv/excel/mysql/)
- [x] Cookie自动关联
- [x] 基于yaml文件的静态配置
- [x] 基于环境变量的动态配置



## 安装
1. 获取本项目代码
```
git clone git@github.com:dongfangtianyu/yiranAPITest.git
```
   

2. 安装依赖
```
pip install -r requirements.txt
```
3. 启动项目
```
pytest
```


## 修改配置
配置文件存放：
- 