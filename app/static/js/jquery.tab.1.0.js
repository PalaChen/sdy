;(function($){
	$.fn.tab=function(options){

		var defaults={
			//各种参数和属性
			colorChangeClass:'colorChange',//class属性
			eventType:'click',//事件属性
			fiUl:'#fiUl li',
			thDiv:'#thDiv div'
		}
		var options=$.extend(defaults,options);

		this.each(function(){
			//实现功能的代码
			var _this=$(this);
			_this.find(options.fiUl).bind(options.eventType,function(){
				$(this).addClass(options.colorChangeClass).siblings().removeClass(options.colorChangeClass);
				//$(this).parent().siblings().find('div').eq($(this).index()).show().siblings().hide();
				var index = $(this).index();
				_this.find(options.thDiv).eq(index).show().siblings().hide();
			});
		});
	}
})(jQuery);