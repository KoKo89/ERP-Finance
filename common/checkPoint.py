"""
# File       : checkPoint.py
# Description：重写unittest断言方法,解决断言失败不再继续执行的问题
"""
import unittest
class CheckPoint(unittest.TestCase):
    def __init__(self,  methodName='runTest'):
        super(CheckPoint, self).__init__(methodName) #继承父类的初始化方法，方法名字随便定义
        self.flag = 0
        self.msg = []
        
 
    # 基本的布尔断言：要么正确，要么错误的验证
    def checkAssertEqual(self, arg1, arg2, msg=None):
        """验证arg1=arg2，不等则fail"""
        try:
            self.assertEqual(arg1, arg2, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkAssertNotEqual(self, arg1, arg2, msg=None):
        """验证arg1 != arg2, 相等则fail"""
        try:
            self.assertNotEqual(arg1, arg2, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
 
    def checkAssertTrue(self, expr, msg=None):
        """验证expr是true，如果为false，则fail"""
        try:
            self.assertTrue(expr, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkAssertFalse(self, expr, msg=None):
        """验证expr是false，如果为true，则fail"""
        try:
            self.assertFalse(expr, msg)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
    
    
     # 比较断言：比较两个变量的值
    def checkAssertGreater(self, first, second, msg=None):
        """验证first > second，否则fail"""
        try:
            self.assertGreater(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkAssertGreaterEqual(self, first, second, msg=None):
        """"验证first >= second，否则fail"""
        try:
            self.assertGreaterEqual(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkAssertLess(self, first, second, msg=None):
        """"验证first < second，否则fail"""
        try:
            self.assertLess(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkAssertLessEqual(self, first, second, msg=None):
        """"验证first <= second，否则fail"""
        try:
            self.assertLessEqual(first, second)
        except Exception as e:
            self.flag += 1
            self.msg.append("\n{}".format(msg))
            print(e)
            
    def checkTestResult(self):
        """获取用例执行结果，断言flag是否为0，不为0说明测试用例中存在断言失败"""
        return self.assertEqual(self.flag, 0, "{}".format(self.msg))