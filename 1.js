getCsrfToken:function(){
var a=CKEDITOR.tools.getCookie("ckCsrfToken"); if(!a||40!=a.length){
var a=[],b="";
if(window.crypto&&window.crypto.getRandomValues)
a=new Uint8Array(40),