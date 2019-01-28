## 1. 用户管理

### 1.1注册

​		

### 1.2登录

#### 	1.2.1 获取QQ登录地址

接口链接

​	URL地址：/oauth/qq/authorization/?next=xxx

http请求方式:

​		 GET

​请求参数

| 参数名 | 类型 | 是否必须 |                 说明                 |
| :----: | :--: | :------: | :----------------------------------: |
|  net   | str  |    否    | 用户QQ登录成功后进入爱美丽商城的地址 |

返回说明

```json
{
    "login_url": "https://graph.qq.com/oauth2.0/authorize?response_type=code&client_id=101474184&redirect_uri=http%3A%2F%2Fwww.meiduo.site%3A8080%2Foauth_callback.html&state=%2Fuser_center_info.html&scope=get_user_info
}
```



## 2.商品管理





## 3.购物车管理



## 4.订单管理

## 5:支付管理



