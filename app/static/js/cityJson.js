var province=[]
var city=[]
var area=[]


$(function(){
	$.ajax({
		url:'/get_city.html',
		type:'GET',
		success:function(arg){
			if (arg['status']==200){
				console.log(arg['message'])
				var message=arg['message']
				province = message['province']
				city = message['city']
				area = message['area']
			}
		}
	})
})



