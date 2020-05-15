var product = $(".add_product")

product.click(function(){
    $.ajax({url: "/index/add_product_to_basket",
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
    quantity = this.id + "_quantity"
    $("#" + quantity).text(function(index, text){
        return parseInt(text) - 1
    })
});