### face-recognition

#### 基于face_recognition提供人脸验证服务

##### 关于部署

```shell script

#项目依赖
face_recognition
flask
elasticsearch

#python 版本
> 3.6
```

##### 接口文档

#人脸识别API目录

1\. 人脸注册
2\. 人脸比对

---

**1\. 人脸注册**
###### 接口功能
> 注册到人脸库

###### URL
> [http://wangmengdev.qicp.io:20619/register)

###### 支持格式
> form-data

###### HTTP请求方式
> POST

###### 请求参数
> |参数|必选|类型|说明|
|:-----  |:-------|:-----|-----                               |
|name    |ture    |string|姓名                         |
|img    |true    |file   |图片文件|

###### 返回字段
> |返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|code   |int    |response code   |
|msg  |string | reponse message                      |

###### 接口示例

![avatar](https://i.loli.net/2019/12/21/pRNkjVZUx5hA8Eq.png)

---

**2\. 人脸比对**
###### 接口功能
> 用于人脸比对

###### URL
> [http://wangmengdev.qicp.io:20619/check)

###### 支持格式
> form-data

###### HTTP请求方式
> POST

###### 请求参数
> |参数|必选|类型|说明|
|:-----  |:-------|:-----|-----                               |
|img    |true    |file   |图片文件|

###### 返回字段
> |返回字段|字段类型|说明                              |
|:-----   |:------|:-----------------------------   |
|code   |int    |response code   |
|msg  |string | reponse message                      |
|data  |object | reponse data                      |

###### 接口示例

![avatar](https://i.loli.net/2019/12/22/qZBcOn6DW4MPI7m.png)
