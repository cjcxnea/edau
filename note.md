## 提示词

首先，充分理解所有的文件结构和代码内容，忽略掉note.md文件，此文件不参与任何功能实现。

#### 给v1.html增加查询验证功能

1. 用户在考试科目下拉选择框选择的信息，与文件夹json/user.json中的testSub数据进行匹配验证
2. 用户在姓名输入框输入的信息，与文件夹json/user.json中的uname数据进行匹配验证
3. 用户在证件号码/准考证号输入框输入的信息，与文件夹json/user.json中的idCard或者examNum其中任意一个数据进行匹配验证
4. 以上验证都通过后，用户点击.btn button查询按钮，跳转到score.html页面,同时不需要将用户信息存储到localStorage中。验证失败时，提示用户输入正确的信息
5. 用于新增以上功能的js代码写入到js/index.js文件中，并在js代码中加上注释说明

#### 修改score.js中的问题

1. score.js是给score.html页面使用的，用于渲染用户信息，敏感信息脱敏以及返回index.html页面，所有的改动都必须基于已有的代码进行
2. 页面加载时，直接将文件夹json/user.json中的用户信息一一对应的渲染到score.html页面的对应位置，需要渲染的内容有：
   1. #test-sub 对应 testSub数据
   2. #user-name 对应 uname数据
   3. #user-idcard 对应 idCard数据
   4. #user-school 对应 schoolName数据
   5. #score-exam-num 对应 examNum数据
   6. #score-total 对应 totalScore数据
   7. #score-listening 对应 listening数据
   8. #score-reading 对应 reading数据
   9. #score-writing 对应 writing数据
   10. #speaking-exam-num 对应 speakingExamNum数据
   11. #speaking-score 对应 speakingScore数据
3. 每次加载页面时，都需要从文件夹json/user.json中读取用户信息，根据用户输入的查询信息，从用户信息中提取出对应的用户信息，渲染到score.html页面的对应位置，不需要存储到localStorage中
4. 必须做到已经完成数据渲染的信息，在页面刷新后，仍然能够显示在score.html页面的对应位置
5. score.js已有的从localStorage中读取用户信息的代码，需要调整以满足以上要求
6. 改动的js代码都加上注释说明

