
var button = document.querySelector(".lucky-btn input");


button.addEventListener('click',function(){
   
    var form = document.getElementsByTagName("form");
   
    // <input type="hidden" name="btnI" value="I">
    var element = document.createElement("input");
    
    var type = document.createAttribute("type");
    type.value = "hidden";
    element.setAttributeNode(type);

    var name = document.createAttribute("name");
    name.value = "btnI";
    element.setAttributeNode(name);

    var val = document.createAttribute("value");
    val.value = "I";
    element.setAttributeNode(val);

    form[0].appendChild(element);

}); 
