$(function(){
	//全服务分类二级导航右侧内容上下局中
	$(".iSubNavRi > li").each(function(){

		var ThisH = $(this).height();
		var ThisChildrenH = $(this).children(".snrText").height();

		$(this).children(".snrText").css({
			"margin-top":-ThisChildrenH/2
		});
	});

	navHover();
	function navHover(){

		var bBut = true;
		var iSubNavDivZ = "iSubNavDivZ";
		var active = "active";
		var noIsHome = "noIsHome";
		var kfwanimate = "kfwanimate";
		var classification1 = "classification1";
		var overflowInherit = "headerOverflowInherit";
		var iNavlis = $(".iNav li");
		var iNavLi = $(".iNav li");
		var kfwNaSuba = $(".kfwNaSub");
		var iSubNavdiv = $(".iSubNav > div");
		var kfwNaSubSub = $(".kfwNaSubSub");
		var aninmatHover = $(".kfwNaSubSub > .iSubNav > div");
		var kfwNaBorder = $(".kfwNaSubSub > .kfwISubNav");
		var noIsHomeObj = $(".kfwNaSub .kfwNaSubSub");
		var classification = $(".kfwNaSub > a .classification");

		//全服务分类二级导航效果
		iNavlis.on("mouseenter mouseleave",function(e){

			var index = $(this).index();
			var iNavBbj = $(this).parents(".kfwISubNav").next(".iSubNav").children("div");
			var kfwNaSubSubObj = $(this).parents(".kfwNaSubSub");

			if (e.type == "mouseenter") {
				iNavBbj.eq(index).addClass(iSubNavDivZ);
				kfwNaSubSubObj.addClass(overflowInherit);
			}else if (e.type == "mouseleave") {
				iNavBbj.removeClass(iSubNavDivZ);
			};
		});
		//全服务分类二级导航右侧效果
		iSubNavdiv.on("mouseenter mouseleave",function(e){

			var index1 = $(this).index();

			if (e.type == "mouseenter") {
				$(this).addClass(iSubNavDivZ);
				iNavlis.eq(index1).addClass(active);
			}else if (e.type == "mouseleave") {
				$(this).removeClass(iSubNavDivZ);
				iNavlis.removeClass(active);
			};
		});

		//鼠标移进导航区和移出导航区时效果
		kfwNaSubSub.on("mouseenter mouseleave",function(e){
			if (e.type == "mouseenter") {
				aninmatHover.removeClass(kfwanimate);
				kfwNaBorder.addClass(active);
				classification.addClass(classification1);
			}else if (e.type == "mouseleave") {
				aninmatHover.addClass(kfwanimate);
				kfwNaBorder.removeClass(active);
				iNavLi.removeClass(overflowInherit);
				classification.removeClass(classification1);
			};
		});

		//全服务分类导航收起和展开效果
		kfwNaSuba.on("mouseenter mouseleave",function(e){
			if (e.type == "mouseenter") {
				$(this).children(".kfwNaSubSub").addClass(noIsHome);
			}else if (e.type == "mouseleave") {
				$(this).children(".kfwNaSubSub").removeClass(noIsHome);
				iNavLi.parents(".kfwNaSubSub").removeClass(overflowInherit);
			};
			e.stopPropagation();
		});
	}
	
	$('.photoSrcClick').click(function(){
		$(".eventTopA").hide('fast');
		return false;
	});
});