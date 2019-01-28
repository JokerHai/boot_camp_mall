## Bootcamp

#### 使用说明：

​		项目根目录下 .env.example，是项目环境变量配置例子，按照自身服务地址做相应配置

#### celery使用说明



#### 前端启动说明

    ​	可以使用前端node.js 提供的服务器live-server作为前端开发服务器使用。

安装node.js的版本控制工具nvm，在终端中执行

      ```
      curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
      ```

**重新进入终端**，使用nvm安装最新版本的node.js

    ```linux
    nvm install node
    ```

安装live-server

    ```
    npm install -g live-server
    ```

使用

    ```
    # 在静态文件目录front_end_pc下执行
    live-server
    ```

live-server运行在8080端口下，可以通过`127.0.0.1:8080`来访问静态页面。



##### 详细接口文档：https://github.com/JokerHai/boot_camp_mall/wiki/bootcamp-documentation
