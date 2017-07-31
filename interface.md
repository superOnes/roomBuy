# 接口设计
### 手机部分
#### 顾客登陆
标题|内容
---:|---|
url:|http://localhost:8000/acc/cuslog/
method:|POST
params:|userid(顾客在user表中的username),protime
return:|JSON

#### 顾客退出
标题|内容
---:|---|
url:|http://localhost:8000/acc/cusout/
method:|POST
params:|userid(顾客在user表中的username)
return:|JSON

#### 显示协议
标题|内容
---:|---|
url:|http://localhost:8000/app/prodel/
method:|GET
params:|tel,personId,id(活动id)
return:|JSON

#### 显示活动
标题|内容
---:|---|
url:|http://localhost:8000/app/detail/
method:|GET
params:|userid(顾客在user表中的username),id(活动id)
return:|JSON

#### 车位/房源 楼号列表
标题|内容
---:|---|
url:|http://localhost:8000/app/houses/
method:|GET
params:|userid(顾客在user表中的username),id(活动id)
return:|JSON

#### 车位/房源 单元列表
标题|内容
---:|---|
url:|http://localhost:8000/app/unit/
method:|GET
params:|userid(顾客在user表中的username),building,id(活动id)
return:|JSON

#### 车位/房源 房号列表
标题|内容
---:|---|
url:|http://localhost:8000/app/houselist/
method:|GET
params:|userid(顾客在user表中的username),building,unit,id(活动id)
return:|JSON

#### 车位/房源 详情
标题|内容
---:|---|
url:|http://localhost:8000/app/houseinfo/
method:|GET
params:|userid(顾客在user表中的username),house(车位/房间号)
return:|JSON

#### 添加收藏
标题|内容
---:|---|
url:|http://localhost:8000/app/addfollow/
method:|POST
params:|userid(顾客在user表中的username),house(车位/房间号)
return:|JSON

#### 取消收藏
标题|内容
---:|---|
url:|http://localhost:8000/app/cancelfollow/
method:|POST
params:|userid(顾客在user表中的username),house(车位/房间号)
return:|JSON

#### 用户收藏列表信息
标题|内容
---:|---|
url:|http://localhost:8000/app/followlist/
method:|GET
params:|userid(顾客在user表中的username)
return:|JSON

#### 订单确认
标题|内容
---:|---|
url:|http://localhost:8000/app/orderconfirm/
method:|POST
params:|userid(顾客在user表中的username),house(车位/房间号)
return:|JSON

#### 订单中协议
标题|内容
---:|---|
url:|http://localhost:8000/app/orderpro/
method:|GET
params:|userid(顾客在user表中的username)
return:|JSON

#### 订单列表
标题|内容
---:|---|
url:|http://localhost:8000/app/orderslist/
method:|GET
params:|userid(顾客在user表中的username)
return:|JSON

#### 订单详情
标题|内容
---:|---|
url:|http://localhost:8000/app/orderinfo/
method:|GET
params:|userid(顾客在user表中的username),orderid
return:|JSON