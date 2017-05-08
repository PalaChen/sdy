
	var PROVINCE_ID = "0"; //省份ID
	var CITY_ID = "0"; //城市ID
	var AREA_ID = "0"; //地区ID
	var urlkey = "company"; //商品关键字
	var provider_list_position = "1"; //服务商显示位置(1:侧边栏，2右侧主框架)

	var CAN_BUY_AREA; //可以购买地区
	var SHOWAREA; //是否显示地区
	var COSTPRICE; //市场价格
	/**
	 * 自动ajax请求商品的价格地区相关信息
	 */
	$.ajax({
		type: "GET",
		url: '/product/productPriceAndArea/uk/company/pr/' + PROVINCE_ID + '/ct/' + CITY_ID + '/ar/' + AREA_ID,
		data: "",
		async: false,
		beforeSend: function () {
			//发送ajax请求数据之前初始化设置
			beforeRequest();
		},
		complete: function (data) {
			//发送ajax请求数据成功之后设置
			completeRequest();
		},
		success: function (result) {
			$('#defaultRegion').remove();
			$('.default-btn').remove();
			$('.btn').show();
			//上线商品
			if (result.isOnLine) {
				$('#productOnLine').show();
				$('#productOffLine').hide();
				$('#productOnLine2').show();
				$('#productOffLine2').hide();

				PROVINCE_ID = result.pca.province;
				CITY_ID = result.pca.city;
				AREA_ID = result.pca.area;

				SHOWAREA = result.showArea;
				CAN_BUY_AREA = result.canBuyArea;

				//设置 市场价
				if (result.costprice != '') {
					$("#costprice2").html('￥' + result.costprice);
					$("#costprice").show();
				}
				//设置 购买价格
				if (result.productPrice != '') {
					$(".t-productprice").html('￥<font>' + result.productPrice[0] + '</font>' + result.productPrice[1]);

					$('.t-vipdiscountpricediv').hide();
					if (result.vipPrice[0])
					{
						if (result.legalvip)
						{
							$(".t-vipdiscountprice").html('<span>￥' + result.vipPrice[0] + result.vipPrice[1] + '</span>' + '&nbsp;&nbsp;您已开通法律顾问会员，支付时会自动为您优惠');
						}
						else
						{
							$(".t-vipdiscountprice").html('<span>￥' + result.vipPrice[0] + result.vipPrice[1] + '</span>' + '&nbsp;&nbsp;<a href="/legalvip">开通法律顾问会员</a>，享受9折优惠');
						}
						$('.t-vipdiscountpricediv').show();
					}
				}
				// 费用说明
				result.officefee = 0; // 2017/1/16，不再显示官费说明
				$('.t-vipdiscountpricediv2').hide();
				if (result.officefee > 0)
				{
					$(".t-vipdiscountprice2").html('官费<span>&nbsp;￥' + result.officefee + '元</span>&nbsp;+&nbsp;服务费<span>&nbsp;￥' + result.servicefee + '元</span>');
					$('.t-vipdiscountpricediv2').show();
				}
				//地区展示处理
				if (SHOWAREA) {
					$(".t-pcatitle").html(result.pca.title);
					$(".t-showarea").show();
				} else {
					$(".t-productprice2").addClass('height60');
				}

				//填充地区至隐藏div
				$("#pcaDiv").html(result.areahtml);

				//ajax获取服务商列表
				getProviderList(urlkey, PROVINCE_ID, CITY_ID, AREA_ID);
			} else {
				//下线商品
				$('#productOnLine').hide();
				$('#productOffLine').show().html(result.htm);
				$('#productOnLine2').hide();
				$('#productOffLine2').show();
			}
		},
		error: function (data) {
		}
	});

	/**
	 * 请求成功前数据初始化
	 */
	function beforeRequest(){
		// If you need to do something before ajax request
	}

	/**
	 * 请求成功后数据恢复
	 */
	function completeRequest(){
		//If you need to do something after ajax request completed
		if (SHOWAREA) {
			var diqu1 = $("#diqu1");
			var diqu2 = $("#diqu2");
			selectProvince(diqu1[0], PROVINCE_ID, CAN_BUY_AREA.province[PROVINCE_ID].title, CAN_BUY_AREA.area[CITY_ID][AREA_ID].title);
			selectProvince(diqu2[0], PROVINCE_ID, CAN_BUY_AREA.province[PROVINCE_ID].title, CAN_BUY_AREA.area[CITY_ID][AREA_ID].title);

			if (-1 == $.inArray(PROVINCE_ID, [1,2,9,22])) {
				selectCity(diqu1[0], CITY_ID, CAN_BUY_AREA.city[PROVINCE_ID][CITY_ID].title, CAN_BUY_AREA.area[CITY_ID][AREA_ID].title);
				selectCity(diqu2[0], CITY_ID, CAN_BUY_AREA.city[PROVINCE_ID][CITY_ID].title, CAN_BUY_AREA.area[CITY_ID][AREA_ID].title);
			}
		}
	}

	/**
	 * 根据商品\省份\城市\地区获取服务商的列表
	 * @param uk 商品关键字
	 * @param pr 省份ID
	 * @param ct 城市ID
	 * @param ar 地区ID
	 */
	function getProviderList( uk, pr, ct, ar ) {
		$.ajax({
			type: "GET",
			url: '/product/ajaxProviderList/uk/'+uk+'/pr/' + pr + '/ct/' + ct + '/ar/' + ar,
			data: "",
			dataType: "json",
			success: function(result){
				if( provider_list_position == "1" ){
					$(".provider-list").html(result);
				}else if( provider_list_position == "2" ){
					$(".product-detail-wrapper").append(result);
				}
			}
		});
	}

	/**
	 * 地区tab切换
	 */
	$("body").on('click', '.stock-tab > li', function(){
		var i = $(this).index();
		$(this).addClass('active');
		$(this).siblings().each(function(){ $(this).removeClass('active') });
		$(this).parents('.stock-select').eq(0).find('.stock-con > ul').each(function(index){
			$(this).hide();
			if (index == i){
				$(this).show();
			}
		});
	});

	function selectProvince(self, pid, ptitle, ctitle)
	{
		ctitle = ctitle || '请选择';
		// tab
		var tabdiv = $(self).parents('.stock-select').eq(0).children(".stock-tab");
		var condiv = $(self).parents('.stock-select').eq(0).children(".stock-con");
		var provinceToCity = {
				'1':[3302,'北京市'],
				'2':[3303,'天津市'],
				'9':[3304,'上海市'],
				'22':[3305,'重庆市']
		};
		var tabhtml = '<li><a href="javascript:void(0)"><em>'+ptitle+'</em><i></i></a></li>' +
			'<li class="active"><a href="javascript:void(0)"><em>'+ctitle+'</em><i></i></a></li>';
		if ('undefined' != typeof(provinceToCity[pid])) {
			var conhtml = $("#provinceDiv").html() + $("#areaDiv" + provinceToCity[pid][0]).html();
		}else{
			var conhtml = $("#provinceDiv").html() + $("#cityDiv" + pid).html();
		}
		tabdiv.html(tabhtml);
		condiv.html(conhtml);

	}

	function selectCity(self, cid, ctitle, atitle)
	{
		atitle = atitle || '请选择';
		// tab
		var tabdiv = $(self).parents('.stock-select').eq(0).children(".stock-tab");
		var condiv = $(self).parents('.stock-select').eq(0).children(".stock-con");

		var tabhtml = '<li class="active"><a href="javascript:void(0)"><em>'+atitle+'</em><i></i></a></li>';
		var conhtml = $("#areaDiv" + cid).html();
		tabdiv.children("li").each(function(i){
			 $(this).removeClass('active');
			 if (1 == i) {
				$(this).find('em').eq(0).html(ctitle);
			 }
			 if (2 == i) {
				$(this).remove();
			 }
		});
		condiv.children("ul").each(function(i){
			 $(this).hide();
			 if (2 == i) {
				$(this).remove();
			 }
		});
		tabdiv.append(tabhtml);
		condiv.append(conhtml);
	}

    setSelectHerf();
	function setSelectHerf() {
		province = PROVINCE_ID;
		city = CITY_ID;
		area = AREA_ID;
		urlkey = urlkey || 'company';

        $.ajax({
            type: "POST",
            url: "/provider/area",
            data: "areaids="+ $('#areaids').val(),
            success: function(msg){
                var href = '/provider/'+urlkey+'.html?pr='+province+'&ct='+city+'&ar=' + area +'&cts='+ msg;
                $(".select-provider").attr("href",href);
            }
        });
	}

	/**
	 * 点击服务商跳转方法
	 * @param province 省份
	 * @param city 城市
	 * @param area 地区
	 * @param urlkey 商品url关键字
	 * @param newpage 是否打开新的页面
	 */
	function goSelectProvider(province, city, area, urlkey, newpage, showarea)
	{
		province = province || PROVINCE_ID;
		city = city || CITY_ID;
		area = area || AREA_ID;
		urlkey = urlkey || 'company';
		newpage = newpage || false;
		showarea = showarea || SHOWAREA;
		$.ajax({
			type: "POST",
			url: "/provider/area",
			data: "areaids="+ $('#areaids').val(),
			success: function(msg){
				jumpTo(newpage, '/provider/'+urlkey+'.html?pr='+province+'&ct='+city+'&ar=' + area +'&cts='+ msg );
			}
		});
	}

	/**
	 * 跳转至服务商选择页面
	 */
	function jumpTo(_openNew, _jumpUrl){
		if(_openNew){
			window.open(_jumpUrl);
		}else{
			window.location.href = _jumpUrl;
		}
	}


