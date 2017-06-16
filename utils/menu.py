from reposition import models
import re


def get_cate_list():
    """
    获取分类信息
    :param cate_list:
    :return:
    """
    """
    获取分类信息
    :param cate_list:
    :return:
    """

    cate_obj = models.ProductCategory.objects.all().order_by('root_id', 'parent_id', '-sort')
    cate_list = []
    for row in cate_obj:
        if row.root_id == 0 and row.parent_id == 0:
            cate_list.append({(row.id, row.name): []})
        elif 0 < row.root_id < 9999:
            for index, cate in enumerate(cate_list):
                for k in cate.keys():
                    if k[0] == row.root_id:
                        cate_list[index][k].append({(row.id, row.name): []})
        elif row.parent_id > 0:
            for index, cate_1 in enumerate(cate_list):
                for k, seconde_cate in cate_1.items():
                    for index_1, cate_2 in enumerate(seconde_cate):
                        for k1 in cate_2.keys():
                            if k1[0] == row.parent_id:
                                cate_list[index][k][index_1][k1].append((row.id, row.name))

    return cate_list


def shop_number(request):
    user_info = request.session.get('user_info')
    shop_list = request.session.get('shop_list')
    if not user_info:
        user_info = {}
    if not shop_list:
        user_info['shop_number'] = 0
    else:
        user_info['shop_number'] = len(shop_list)
    return user_info


class MenuHelper(object):
    def __init__(self, request, email):
        # 当前请求的request对象
        self.request = request
        # # 当前用户邮箱
        # self.email = email
        # 当前用户角色id
        self.email = email

        # 获取当前URL
        self.current_url = request.path_info

        # 获取当前用户的所有权限
        self.permission2action_dict = None
        # 获取在菜单中显示的权限
        self.menu_leaf_list = None
        # 获取所有菜单
        self.menu_list = None

        self.session_data()

    # 　从session中取数据
    def session_data(self):
        permission_dict = self.request.session.get('permission_info')
        # print('session中权限字典', permission_dict)
        if permission_dict:
            self.permission2action_dict = permission_dict['permission2action_dict']
            self.menu_leaf_list = permission_dict['menu_leaf_list']
            self.menu_list = permission_dict['menu_list']
        else:
            # 获取当前用户的角色列表
            # role_querSet = models.Role.objects.filter(employee2role__employee__email=self.email)
            role_querSet = models.Role.objects.filter(id=self.email)
            # print('当前用户角色列表:', role_querSet)
            # 获取当前用户的权限列表（URL+Action）
            # v = [
            #     {'url':'/inde.html','code':'GET'},
            #     {'url':'/inde.html','code':'POST'},
            #     {'url':'/order.html','code':'PUT'},
            #     {'url':'/order.html','code':'GET'},
            # ]
            # v = {
            #     '/inde.html':['GET']
            # }
            permission2action_list = models.Permission2Action.objects. \
                filter(permission2action2role__role__in=role_querSet). \
                values('permission__url', 'action__code').distinct()

            # 　将数据转换为指定格式的字典
            permission2action_dict = {}
            for item in permission2action_list:
                # print(item)
                if item['permission__url'] in permission2action_dict:
                    permission2action_dict[item['permission__url']].append(item['action__code'])
                else:
                    permission2action_dict[item['permission__url']] = [item['action__code'], ]
            # permission2action_dict的值
            # {'/admin/user/recommend.html': ['get', 'post', 'del', 'put'], '/admin/org/position.html': ['get', 'post', 'del', 'put'],}


            # 获取菜单的叶子节点，即：菜单的最后一层应该显示的权限
            menu_leaf_list = list(models.Permission2Action.objects.filter(permission2action2role__role__in=role_querSet) \
                                  .exclude(permission__menu__isnull=True) \
                                  .values('permission_id', 'permission__url', 'permission__caption',
                                          'permission__menu').distinct())
            # 获取所有的菜单列表
            menu_list = list(models.Menu.objects.values('id', 'caption', 'parent_id'))
            # print('menu_list--->', menu_list)

            self.request.session['permission_info'] = {
                'permission2action_dict': permission2action_dict,
                'menu_leaf_list': menu_leaf_list,
                'menu_list': menu_list,
            }
            # print('menu_leaf_list-->', menu_leaf_list)
            self.permission2action_list = permission2action_list
            self.menu_leaf_list = menu_leaf_list
            self.menu_list = menu_list

    def menu_data_list(self):

        menu_leaf_dict = {}
        open_leaf_parent_id = None
        # 归并所有的叶子节点
        for item in self.menu_leaf_list:
            item = {
                'id': item['permission_id'],
                'url': item['permission__url'],
                'caption': item['permission__caption'],
                'parent_id': item['permission__menu'],
                'child': [],
                'status': True,  # 是否显示
                'open': False
            }
            if item['parent_id'] in menu_leaf_dict:
                menu_leaf_dict[item['parent_id']].append(item)
            else:
                menu_leaf_dict[item['parent_id']] = [item, ]

            if re.match(item['url'], self.current_url):
                item['open'] = True
                open_leaf_parent_id = item['parent_id']

        # 获取所有菜单字典
        menu_dict = {}
        for item in self.menu_list:
            item['child'] = []
            item['status'] = False
            item['open'] = False
            menu_dict[item['id']] = item

        # 讲叶子节点添加到菜单中
        for k, v in menu_leaf_dict.items():
            menu_dict[k]['child'] = v
            parent_id = k
            # 将后代中有叶子节点的菜单标记为【显示】
            while parent_id:
                menu_dict[parent_id]['status'] = True
                parent_id = menu_dict[parent_id]['parent_id']

        # 将已经选中的菜单标记为【展开】
        while open_leaf_parent_id:
            menu_dict[open_leaf_parent_id]['open'] = True
            open_leaf_parent_id = menu_dict[open_leaf_parent_id]['parent_id']

        # 生成树形结构数据
        result = []
        for row in menu_dict.values():
            if not row['parent_id']:
                result.append(row)
            else:
                menu_dict[row['parent_id']]['child'].append(row)

        return result

    def menu_content(self, child_list):
        response = ""
        tpl = """
             <div class="item">
                <div class="manageBanner">
                    <span class="icon">
                        <i class='glyphicon glyphicon-plus'></i>
                    </span>
                    <span>%s</span>
                </div>
                <ul class="list-unstyled %s">
                    <li class="manageItem">
                        %s
                    </li>
                </ul>
            </div>
        """
        for row in child_list:
            if not row['status']:
                continue
            active = ""
            if row['open']:
                active = "menu_active"
            if 'url' in row:
                response += "<li class='manageItem %s'><a href='%s'>%s</a></li>" % (
                    active, row['url'], row['caption'])
            else:
                title = row['caption']
                content = self.menu_content(row['child'])
                response += tpl % (title, active, content)
        return response

    def menu_tree(self):
        response = ""
        tpl = """
        <div class="item">
            <div class="manageBanner">
                <span class="icon">
                    <i class='glyphicon %s'></i>
                </span>
                <span>%s</span>
            </div>
            <ul class="list-unstyled %s">%s</ul>
        </div>
        """
        for row in self.menu_data_list():
            if not row['status']:
                continue
            active = "hide"
            is_plus = 'glyphicon-plus'
            if row['open']:
                is_plus = 'glyphicon-minus'
                active = ""
            # 第一层第一个
            title = row['caption']
            # 第一层第一个的后代
            content = self.menu_content(row['child'])
            response += tpl % (is_plus, title, active, content)

        return response

    def actions(self):
        """
        检查当前用户是否对当前URL有权访问，并获取对当前URL有什么权限
        """
        action_list = []
        # 当前所有权限
        # {
        #     '/index.html': ['get',post,]
        # }
        # print('循环self.permission2action_dict',self.permission2action_dict)
        for k, v in self.permission2action_dict.items():
            if re.match(k, self.current_url):
                action_list = v  # ['GET',POST,]
                break
            elif '_add.html' in self.current_url:
                k = k.split('.')[0] + '_add.html'
            elif '_del/' in self.current_url:
                k = k.split('.')[0] + '_del/(\d+).html'
            elif '_edit.html' in self.current_url:
                k = k.split('.')[0] + '_edit.html'
            elif '_edit' in self.current_url:
                k = k.split('.')[0] + '_edit/(\d+).html'
            elif '_del.html' in self.current_url:
                k = k.split('.')[0] + '_del.html'

            # print(k, self.current_url)
            if re.match(k, self.current_url):
                action_list = v  # ['GET',POST,]
                break

                ####### 方法一
                # for method in v:
                #     if method == 'get':
                #         pass
                #     elif method == 'post':
                #         k = k.split('.')[0] + '_add.html'
                #     elif v == 'del':
                #         k = k.split('.')[0] + '_del/(\d+).html'
                #     elif v == 'put':
                #         k = k.split('.')[0] + '_edit.html'
                #
                #     if re.match(k, self.current_url):
                #         action_list = method
                #         break

                # print(self.current_url)
                # else:
                #     for method in v:
                #         pass

        return action_list
