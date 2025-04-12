# 关于於菟bot

这里是一个大二（25年）的兰台，20年的暑假接触到的墨魂，让我非常快乐的玩了两年多的单机游戏

直到23年的元旦（本人因为疫情封校刚出来），才得知要停服了，吓得赶紧去加了几个群，包括整理总群、图片整理、自习室、设定集等，也混过几个企划啥的，虽然我的文学功底在理科班算是很好的了，但是却发现同僚们各有才艺，拼尽全力无法匹敌

加上本人在学校各个方面屡屡碰壁，最后机缘巧合下通过兴趣和专业知识接触到了一点bot的东西

从2025.03.22开始使用 **`nonebot2`+`napcat(一键部署/llob)`** 来搭建一个菟菟的bot

因为还不怎么会用，我只在该项目中传自定义的插件，需要的师傅/同僚可以更改


## 配置

服务器or本地主机：用的是阿里云服务器——大学生白嫖版2h4g

系统：debian12.4（本来想用centos7但是发现python支持不行

python3版本：python3.11.2

nonebot2：懒得折腾docker直接起python虚拟环境安装的

napcat：4.7.10，shell一键包

linuxQQ：3.2.16-32793

数据库：一开始使用 mysql 但是后改为 apache + phpmyadmin 便于其他兰台协助录入联诗题库



有懂这些方面的同僚可以自行官网搜索，进阶的可以找一下docker compose的联动部署



## 需求（大饼

- [x] 兰台——qq账户绑定（第一次点卯时自动记录

- [x] 每日点卯，凌晨四点刷新

- [ ] 联诗

  - 连续交互 :heavy_check_mark:

  - 计时功能 :heavy_check_mark:

  - 评价体系（值得一喵） :heavy_check_mark:

  - 题库录入（正在做

    感谢 **设定集企划** 提供的 ~~**五三**~~ <sub>*五年兰台三年联诗*</sub>

- [ ] 飞花令（纯大饼

  正在考虑：

  通过api接入大模型（怕有人工智障

  还是通过数据库存储+学习（过程较慢

  抑或二者结合起来使用

- [x] 戳一戳有回应

  喵~  :heavy_check_mark:

  戳回去（这些协议端奇奇怪怪的api我看蒙了，等我研究研究，怎么onebot和napcat的api不一样阿） :heavy_check_mark:
