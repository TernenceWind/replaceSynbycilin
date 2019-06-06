## Readme

#### 数据说明
`各位老板，这手机质量怎么样？谢谢！<ssssss>还算可以<ssssss>(质量,质量,1)`

`以<ssssss>分割，第一部分是问题，第二部分是答案，第三部分是标注`

`标注部分的三元组，第一部分是属性描述语，aspect term，是原文中出现的词语`

`三元组的第二部分是属性的类别，三元组的第三部分是该属性的情感极性`

----
#### 任务说明
利用哈工大提供的同义词林随机替换原样本中的同义词，构建扩展的样本库，可缓解样本不平衡问题。

输入为样本文件

输出为扩展文件和扩展后的总样本文件


----
#### 文件说明
1.  ltp_data_v3.4.0目录为pyltp的模型文件，约1.1GB的内容，用于进行分词，请自行前往下载。[百度云](https://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#list/path=%2Fltp-models&parentPath=%2F)。
2.  pyltp-0.2.1-cp36-cp36m-win_amd64.whl为pyltp的离线安装包，若要使用务必注意对应版本。
1.  cilin.txt为哈工大同义词词典文件([说明文件](http://read.pudn.com/downloads56/sourcecode/unix_linux/194259/%A1%B6%CD%AC%D2%E5%B4%CA%B4%CA%C1%D6%A3%A8%C0%A9%D5%B9%B0%E6%A3%A9%A1%B7%D1%F9%C0%FD/%A1%B6%CD%AC%D2%E5%B4%CA%B4%CA%C1%D6%A3%A8%C0%A9%D5%B9%B0%E6%A3%A9%A1%B7%CB%B5%C3%F7.pdf),[数据来源](https://github.com/yaleimeng/Final_word_Similarity/blob/master/cilin/V2/cilin.txt#L2))。
