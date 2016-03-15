# UIMS-auto-select-class

运行方法：

JLUSelectCourse.py:

将self.username, self.password字段分别填写自己的用户名和密码， self.course_id填写所选课程id

在命令行中直接运行python JLUSelectCourse.py即可

geventJLUSelectCourse.py：

这个版本速度更快，可以同时选多个课程，但是需要先安装python第三方库gevent

命令行运行：

python geventJLUSelectCourse.py -username 你的用户名 -password 你的密码 -courseid 所选课id

若同时选两门课运行：

python geventJLUSelectCourse.py -username 你的用户名 -password 你的密码 -courseid 所选课程id1 -courseid 所选课课程id2

三门课以此类推

课程id号：

在选课页面右键->审查元素查找对应课程id

如下：

![image](https://github.com/zhaodongzhi/UIMS-auto-select-class/blob/master/CourseidExample.png)



