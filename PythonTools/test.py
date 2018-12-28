import timehutSeleniumToolKit as tstk
import pdb

# pdb.set_trace()
timehutUrl = "https://www.shiguangxiaowu.cn/zh-CN"
a = tstk.timehutSeleniumToolKit(False)
a.fetchTimehutPage(timehutUrl)
a.loginTimehut('mikelhsia@hotmail.com', 'f19811128')
a.whereami()
a.scrollDownTimehutPage(1)
a.whereami(2)
a.scrollDownTimehutPage(2)
a.whereami(3)
a.scrollDownTimehutPage(3)
a.whereami(4)

