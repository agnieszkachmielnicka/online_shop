var product = $(".remove_product")

product.click(function(){
    $.ajax({url: "/index/remove_product_from_basket",
            type: "GET",
            data: {
                product_id : this.id
            },
            success: function(result){
                console.log("success")
            },
            error: function(result) {
                console.log("error")
            }
            });
    this.parentNode.remove()
});