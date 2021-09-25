$('#slider1, #slider2, #slider3').owlCarousel({
    loop: true,
    margin: 20,
    responsiveClass: true,
    responsive: {
        0: {
            items: 1,
            nav: false,
            autoplay: true,
        },
        600: {
            items: 3,
            nav: true,
            autoplay: true,
        },
        1000: {
            items: 5,
            nav: true,
            loop: true,
            autoplay: true,
        }
    }
})

$('.plus-cart').click(function () {

    id = $(this).attr('pid').toString();
    elm = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data : {
            'id' : id,
        },

        success: function (data) {
            elm.innerText =  data.quantity;
            document.getElementById("amount").innerText =  data.amount;
            document.getElementById("totalamount").innerText =  data.amount;
        }
    })
})

$('.minus-cart').click(function () {

    id = $(this).attr('pid').toString();
    elm = this.parentNode.children[2];
    // console.log(id);
    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data : {
            'id' : id,
        },

        success: function (data) {
            
           
            elm.innerText =  data.quantity;
            document.getElementById("amount").innerText =  data.amount;
            document.getElementById("totalamount").innerText =  data.amount;
        }
    })
})